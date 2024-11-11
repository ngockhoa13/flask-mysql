# Sử dụng image Python 3.10 từ Dev Containers của VSCode
FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.12

# Cài đặt PostgreSQL client
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends postgresql-client \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /workspace

# Sao chép file requirements.txt vào container
COPY requirements.txt /workspace/requirements.txt

# Cài đặt các dependencies từ requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# Đảm bảo ứng dụng Flask lắng nghe trên tất cả các địa chỉ IP trong container
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

# Chạy lệnh khởi động Flask
CMD ["flask", "run"]
