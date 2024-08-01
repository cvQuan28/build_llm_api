# Sử dụng hình ảnh Python chính thức từ Docker Hub
FROM python:3.9-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn của ứng dụng vào thư mục làm việc
COPY . /app/

# Expose port 5000 để Flask có thể chạy
EXPOSE 5000

# Khởi động ứng dụng
CMD ["python", "app.py"]