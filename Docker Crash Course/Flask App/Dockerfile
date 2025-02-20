FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . . 

EXPOSE 5000

ENV DEBUG=False
ENV PORT=5000
ENV LOG_FILE=/data/logs/log.txt

CMD ["python3", "app.py"]
