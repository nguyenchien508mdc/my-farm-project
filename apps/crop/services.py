# apps/crop/services.py
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Crop, CropType, CropStage
from apps.farm.models import Farm
from apps.field_monitoring.models import SoilMeasurement, WeatherRecord

class CropService:
    @staticmethod
    def create_crop(farm_id, crop_type_id, **kwargs):
        """
        Tạo mới một crop với các thông số cơ bản
        """
        farm = Farm.objects.get(pk=farm_id)
        crop_type = CropType.objects.get(pk=crop_type_id)
        
        # Validate diện tích
        area = kwargs.get('area', 0)
        if area <= 0:
            raise ValidationError("Diện tích phải lớn hơn 0")
        
        # Tự động tính ngày thu hoạch dự kiến nếu có ngày trồng
        planting_date = kwargs.get('planting_date')
        harvest_date = kwargs.get('harvest_date')
        
        if planting_date and not harvest_date:
            harvest_date = planting_date + timezone.timedelta(days=crop_type.growth_duration)
            kwargs['harvest_date'] = harvest_date
        
        crop = Crop.objects.create(
            farm=farm,
            crop_type=crop_type,
            **kwargs
        )
        
        # Tạo các giai đoạn mặc định
        CropService._create_default_stages(crop)
        
        return crop

    @staticmethod
    def _create_default_stages(crop):
        """Tạo các giai đoạn mặc định cho cây trồng"""
        default_stages = [
            {'name': 'Chuẩn bị đất', 'days_after_planting': 0, 'duration': 7},
            {'name': 'Gieo trồng', 'days_after_planting': 7, 'duration': 3},
            {'name': 'Chăm sóc ban đầu', 'days_after_planting': 10, 'duration': 20},
            {'name': 'Phát triển', 'days_after_planting': 30, 'duration': crop.crop_type.growth_duration - 50},
            {'name': 'Thu hoạch', 'days_after_planting': crop.crop_type.growth_duration - 20, 'duration': 20},
        ]
        
        planting_date = crop.planting_date or timezone.now().date()
        
        for stage in default_stages:
            start_date = planting_date + timezone.timedelta(days=stage['days_after_planting'])
            end_date = start_date + timezone.timedelta(days=stage['duration'])
            
            CropStage.objects.create(
                crop=crop,
                name=stage['name'],
                start_date=start_date,
                end_date=end_date,
                description=f"Giai đoạn {stage['name']} của {crop.crop_type.name}"
            )

    @staticmethod
    def update_crop_status(crop_id, status):
        """
        Cập nhật trạng thái cây trồng
        """
        crop = Crop.objects.get(pk=crop_id)
        valid_transitions = {
            'planned': ['seedling'],
            'seedling': ['growing', 'failed'],
            'growing': ['harvested', 'failed'],
            'harvested': [],
            'failed': [],
        }
        
        if status not in valid_transitions.get(crop.status, []):
            raise ValidationError(f"Không thể chuyển từ {crop.status} sang {status}")
        
        crop.status = status
        
        # Nếu chuyển sang trạng thái thu hoạch, cập nhật ngày thu hoạch
        if status == 'harvested' and not crop.harvest_date:
            crop.harvest_date = timezone.now().date()
        
        crop.save()
        return crop

    @staticmethod
    def record_yield(crop_id, actual_yield):
        """
        Ghi nhận năng suất thực tế
        """
        crop = Crop.objects.get(pk=crop_id)
        
        if crop.status != 'harvested':
            raise ValidationError("Chỉ có thể ghi nhận năng suất khi cây đã thu hoạch")
        
        crop.actual_yield = actual_yield
        crop.save()
        return crop

    @staticmethod
    def get_crop_health(crop_id):
        """
        Đánh giá sức khỏe cây trồng dựa trên các chỉ số
        """
        crop = Crop.objects.get(pk=crop_id)
        latest_soil = SoilMeasurement.objects.filter(farm=crop.farm).latest('date_tested')
        latest_weather = WeatherRecord.objects.filter(farm=crop.farm).latest('date')
        
        # Đánh giá điều kiện đất
        soil_score = 0
        if (latest_soil.ph >= crop.crop_type.optimal_ph_min and 
            latest_soil.ph <= crop.crop_type.optimal_ph_max):
            soil_score += 1
        
        # Đánh giá điều kiện thời tiết
        weather_score = 0
        if (latest_weather.temperature >= crop.crop_type.optimal_temperature_min and 
            latest_weather.temperature <= crop.crop_type.optimal_temperature_max):
            weather_score += 1
        
        total_score = soil_score + weather_score
        health_status = "Tốt" if total_score == 2 else "Khá" if total_score == 1 else "Kém"
        
        return {
            'health_status': health_status,
            'soil_condition': {
                'ph': latest_soil.ph,
                'optimal_ph': f"{crop.crop_type.optimal_ph_min}-{crop.crop_type.optimal_ph_max}"
            },
            'weather_condition': {
                'temperature': latest_weather.temperature,
                'optimal_temperature': f"{crop.crop_type.optimal_temperature_min}-{crop.crop_type.optimal_temperature_max}°C"
            }
        }

    @staticmethod
    def complete_stage(stage_id):
        """
        Đánh dấu hoàn thành giai đoạn
        """
        stage = CropStage.objects.get(pk=stage_id)
        stage.completed = True
        stage.end_date = timezone.now().date()
        stage.save()
        return stage

class CropTypeService:
    @staticmethod
    def create_crop_type(name, growth_duration, temp_min, temp_max, ph_min, ph_max, **kwargs):
        """
        Tạo mới một loại cây trồng
        """
        if growth_duration <= 0:
            raise ValidationError("Thời gian sinh trưởng phải lớn hơn 0")
        
        if temp_min >= temp_max:
            raise ValidationError("Nhiệt độ tối thiểu phải nhỏ hơn tối đa")
            
        if ph_min >= ph_max:
            raise ValidationError("Độ pH tối thiểu phải nhỏ hơn tối đa")
            
        crop_type = CropType.objects.create(
            name=name,
            growth_duration=growth_duration,
            optimal_temperature_min=temp_min,
            optimal_temperature_max=temp_max,
            optimal_ph_min=ph_min,
            optimal_ph_max=ph_max,
            **kwargs
        )
        return crop_type

    @staticmethod
    def recommend_crops(farm_id):
        """
        Gợi ý loại cây trồng phù hợp với điều kiện nông trại
        """
        farm = Farm.objects.get(pk=farm_id)
        latest_soil = SoilMeasurement.objects.filter(farm=farm).latest('date_tested')
        
        recommended = CropType.objects.filter(
            optimal_ph_min__lte=latest_soil.ph,
            optimal_ph_max__gte=latest_soil.ph
        )
        
        return recommended