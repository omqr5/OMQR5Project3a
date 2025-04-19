FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install flask pygal requests

CMD ["python", "app.py"]

EXPOSE 5000
