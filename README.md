# IoT Streaming Pipeline (MQTT → Kafka → Spark)

Một hệ thống streaming real-time để xử lý dữ liệu IoT từ cảm biến nhiệt độ, sử dụng MQTT, Kafka và Apache Spark.

## Kiến trúc hệ thống

```
[Simulator] --MQTT--> [HiveMQ Cloud] --MQTT--> [Bridge] --Kafka--> [Kafka] --Spark--> [Processing]
```

### Các thành phần:

- **Simulator**: Sinh dữ liệu cảm biến nhiệt độ và gửi qua MQTT
- **HiveMQ Cloud**: Public MQTT broker (cloud)
- **Bridge Service**: Lắng nghe MQTT, chuyển dữ liệu sang Kafka topic
- **Kafka**: Lưu trữ và phân phối dữ liệu streaming
- **Spark Structured Streaming**: Đọc dữ liệu từ Kafka, tính trung bình nhiệt độ theo cửa sổ thời gian, phát cảnh báo nếu > 40°C

## Cấu trúc thư mục

```
.
├── README.md
├── docker-compose.yml
├── simulator/
│   ├── simulator.py
│   ├── Dockerfile 
│   └── .env
├── bridge/
│   ├── bridge-mqtt-kafka.py
│   └──  Dockerfile
└── app/
    ├── spark-app.py
    └──  Dockerfile
```

## Cấu hình

### 1. Tạo file environment variables

```bash
vim .env
```

### 2. Cập nhật file `.env` với thông tin HiveMQ của bạn

```env
# MQTT Configuration (HiveMQ Cloud)
MQTT_BROKER=your-hivemq-cluster.hivemq.cloud
MQTT_PORT=8883
MQTT_TOPIC=iot/temperature
MQTT_USERNAME=your-hivemq-username
MQTT_PASSWORD=your-hivemq-password

# Kafka Configuration
KAFKA_BOOTSTRAP=kafka:9092
KAFKA_TOPIC=iot_temperature

## Hướng dẫn chạy

### 1️. Khởi động toàn bộ dịch vụ

```bash
docker compose up -d --build
```

### 2️. Kiểm tra trạng thái các container

```bash
docker compose ps
```

### 3️. Kiểm tra Kafka topic đã được tạo

```bash
docker exec -it kafka kafka-topics.sh \
  --list \
  --bootstrap-server localhost:9092
```

### 4️. Xem dữ liệu từ Kafka (Optional)

```bash
docker exec -it kafka kafka-console-consumer.sh \
  --topic iot_temperature \
  --bootstrap-server localhost:9092 \
  --from-beginning
```

### 6. Chạy Spark Streaming 

```bash
docker exec -it spark-master spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 \
  /opt/bitnami/spark/app/app.py
```

## 📊 Ví dụ output

### Simulator logs:
```
Published: {"temperature": 35.42, "timestamp": "2025-09-21T10:30:05Z"}
Published: {"temperature": 42.18, "timestamp": "2025-09-21T10:30:07Z"}
```

### Bridge logs:
```
Received MQTT message: {"temperature": 35.42, "timestamp": "2025-09-21T10:30:05Z"}
Sent to Kafka topic 'iot_temperature'
```

### Spark Streaming output:
```
+-------------------+------------------+-----+
|window             |avg_temp          |alert|
+-------------------+------------------+-----+
|2025-09-21 10:30:00|35.42            |OK   |
|2025-09-21 10:30:10|42.18            |ALERT|
|2025-09-21 10:30:20|38.95            |OK   |
+-------------------+------------------+-----+
```

## 🔍 Mô tả chi tiết các service

### Simulator Service
- **File**: `simulator/simulator.py`
- **Chức năng**: Sinh dữ liệu nhiệt độ ngẫu nhiên (20-50°C) mỗi 2 giây
- **Output**: JSON message qua MQTT

### Bridge Service  
- **File**: `bridge/bridge-mqtt-kafka.py`
- **Chức năng**: Kết nối MQTT broker và Kafka, chuyển đổi message
- **Input**: MQTT messages từ HiveMQ
- **Output**: Kafka messages đến topic `iot_temperature`

### Spark Application
- **File**: `app/spark-app.py`
- **Chức năng**: 
  - Đọc streaming data từ Kafka
  - Tính trung bình nhiệt độ trong cửa sổ 10 giây
  - Phát cảnh báo khi nhiệt độ > 40°C
- **Output**: Console output với kết quả xử lý

## 📚 Tài liệu tham khảo

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Spark Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [HiveMQ Cloud](https://www.hivemq.com/cloud/)
- [Paho MQTT Python Client](https://github.com/eclipse/paho.mqtt.python)
