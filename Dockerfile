# Sử dụng image Python
FROM python:3.11

# Cài đặt các thư viện cần thiết
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Tạo thư mục ứng dụng và sao chép các file cần thiết
WORKDIR /usr/src/app
COPY . .

# Cài đặt Playwright
RUN python -m playwright install

# Chạy ứng dụng Python
CMD ["python", "app.py"]
