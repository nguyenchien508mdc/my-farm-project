# apps/operations/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.core.models import BaseModel

class TaskCategory(BaseModel):
    name = models.CharField(_("Tên danh mục"), max_length=100)
    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='task_categories')
    description = models.TextField(_("Mô tả"), blank=True)
    color = models.CharField(_("Màu sắc hiển thị"), max_length=20, default='#4CAF50')

    def __str__(self):
        return f"{self.name} ({self.farm.name})"

    class Meta:
        verbose_name = _("Danh mục công việc")
        verbose_name_plural = _("Danh mục công việc")
        unique_together = ('name', 'farm')

class Task(BaseModel):
    PRIORITY_CHOICES = [
        ('low', 'Thấp'),
        ('medium', 'Trung bình'),
        ('high', 'Cao'),
        ('urgent', 'Khẩn cấp'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Chờ thực hiện'),
        ('assigned', 'Đã giao'),
        ('in_progress', 'Đang thực hiện'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]

    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    title = models.CharField(_("Tiêu đề"), max_length=255)
    description = models.TextField(_("Mô tả"), blank=True)
    assigned_by = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    assigned_to = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    start_date = models.DateField(_("Ngày bắt đầu"))
    due_date = models.DateField(_("Hạn hoàn thành"))
    completed_date = models.DateField(_("Ngày hoàn thành"), null=True, blank=True)
    priority = models.CharField(_("Ưu tiên"), max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(_("Trạng thái"), max_length=20, choices=STATUS_CHOICES, default='pending')
    area = models.CharField(_("Khu vực"), max_length=100, blank=True)
    related_object_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('related_object_type', 'related_object_id')

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    class Meta:
        verbose_name = _("Công việc")
        verbose_name_plural = _("Công việc")
        ordering = ['-due_date']
        indexes = [
            models.Index(fields=['farm', 'status']),
            models.Index(fields=['assigned_to', 'due_date']),
        ]

class TaskReport(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='task_reports')
    report_date = models.DateField(_("Ngày báo cáo"), auto_now_add=True)
    content = models.TextField(_("Nội dung báo cáo"))
    progress = models.PositiveIntegerField(_("Tiến độ (%)"), validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"Báo cáo #{self.id} - {self.task.title}"

    class Meta:
        verbose_name = _("Báo cáo công việc")
        verbose_name_plural = _("Báo cáo công việc")
        ordering = ['-report_date']

class TaskAttachment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    task_report = models.ForeignKey(TaskReport, on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    file = models.FileField(_("File đính kèm"), upload_to='task_attachments/')
    description = models.CharField(_("Mô tả"), max_length=255, blank=True)
    uploaded_by = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.file.name}"

    class Meta:
        verbose_name = _("File đính kèm công việc")
        verbose_name_plural = _("File đính kèm công việc")

class Irrigation(BaseModel):
    METHOD_CHOICES = [
        ('drip', 'Tưới nhỏ giọt'),
        ('sprinkler', 'Tưới phun'),
        ('flood', 'Tưới ngập'),
        ('manual', 'Tưới thủ công'),
    ]

    STATUS_CHOICES = [
        ('planned', 'Đã lên kế hoạch'),
        ('in_progress', 'Đang thực hiện'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]

    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='irrigations')
    task = models.OneToOneField(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='irrigation_task')
    date = models.DateField(_("Ngày tưới"))
    method = models.CharField(_("Phương pháp"), max_length=20, choices=METHOD_CHOICES)
    duration = models.PositiveIntegerField(_("Thời gian (phút)"))
    water_amount = models.FloatField(_("Lượng nước (m3)"))
    status = models.CharField(_("Trạng thái"), max_length=20, choices=STATUS_CHOICES, default='planned')
    notes = models.TextField(_("Ghi chú"), blank=True)
    related_crop = models.ForeignKey('crop.Crop', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.get_method_display()} irrigation on {self.date}"

    class Meta:
        verbose_name = _("Tưới tiêu")
        verbose_name_plural = _("Tưới tiêu")
        ordering = ['-date']

class Fertilization(BaseModel):
    STATUS_CHOICES = [
        ('planned', 'Đã lên kế hoạch'),
        ('in_progress', 'Đang thực hiện'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]

    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='fertilizations')
    task = models.OneToOneField(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='fertilization_task')
    date = models.DateField(_("Ngày bón"))
    fertilizer = models.ForeignKey('inventory.InventoryItem', on_delete=models.PROTECT, limit_choices_to={'item_type': 'fertilizer'})
    amount = models.FloatField(_("Lượng bón (kg)"))
    method = models.CharField(_("Phương pháp"), max_length=100)
    status = models.CharField(_("Trạng thái"), max_length=20, choices=STATUS_CHOICES, default='planned')
    notes = models.TextField(_("Ghi chú"), blank=True)
    related_crop = models.ForeignKey('crop.Crop', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Fertilization with {self.fertilizer.name} on {self.date}"

    class Meta:
        verbose_name = _("Bón phân")
        verbose_name_plural = _("Bón phân")
        ordering = ['-date']
