FROM node:16

# Tạo thư mục làm việc
WORKDIR /usr/src/app

# Sao chép package.json và cài đặt các dependencies
COPY package.json ./
RUN npm install

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Mở port
EXPOSE 8080

# Chạy ứng dụng
CMD ["npm", "start"]
