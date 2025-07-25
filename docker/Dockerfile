# docker\Dockerfile
# Sử dụng image chính thức của Python làm base
FROM python:3.11-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Cài đặt hệ thống phụ thuộc
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Sao chép file yêu cầu cài đặt vào container
COPY requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Cấp quyền thực thi cho script khởi động
RUN chmod +x ./docker/entrypoint.sh

# Sử dụng entrypoint để setup DB trước khi chạy lệnh chính
ENTRYPOINT ["./docker/entrypoint.sh"]

# Command mặc định (nếu không override trong docker-compose)
CMD ["gunicorn", "myfarm_project.wsgi:application", "--bind", "0.0.0.0:8000"]
