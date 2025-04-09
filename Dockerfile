FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
