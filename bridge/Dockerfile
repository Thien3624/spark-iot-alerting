FROM python:3.9-slim

WORKDIR /app
COPY bridge-mqtt-kafka.py .
RUN pip install paho-mqtt==1.6.1 kafka-python==2.0.2

CMD ["python", "bridge-mqtt-kafka.py"]
