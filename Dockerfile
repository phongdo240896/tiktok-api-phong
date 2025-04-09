# Docker image có sẵn Chromium + Playwright
FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["node", "app.js"]
