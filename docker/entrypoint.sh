# docker\entrypoint.sh
#!/bin/bash
set -e  # Dừng script nếu có lỗi

echo "🚀 Waiting for database to be ready..."

# Dùng netcat để chờ DB thật sự sẵn sàng trước khi chạy migrate
while ! nc -z $DB_HOST $DB_PORT; do
  echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
  sleep 1
done

echo "📦 Applying database migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Starting server..."
exec gunicorn myfarm_project.wsgi:application --bind 0.0.0.0:8000
