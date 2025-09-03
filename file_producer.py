# file_producer.py

import json
from kafka import KafkaProducer
from tqdm import tqdm

# 카프카 프로듀서 설정
producer = KafkaProducer(
    bootstrap_servers=['localhost:9094', 'localhost:9095', 'localhost:9096'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# TOPIC_NAME = 'user-behavior'
# FILE_PATH = 'dummy_data.json'
TOPIC_NAME = 'test'
FILE_PATH = 'test_dummy_data.json'

def send_data_from_file(filename):
    """파일을 읽어 카프카로 전송하는 함수"""
    print(f"Starting to send data from '{filename}' to Kafka topic '{TOPIC_NAME}'.")
    
    # 전체 라인 수를 세어 진행률을 표시하기 위함
    with open(filename, 'r') as f:
        total_lines = sum(1 for line in f)

    with open(filename, 'r') as f:
        for line in tqdm(f, total=total_lines, desc="Sending to Kafka"):
            try:
                # 각 라인은 하나의 JSON 객체
                message = json.loads(line)
                producer.send(TOPIC_NAME, value=message)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from line: {line.strip()}")
            except Exception as e:
                print(f"An error occurred: {e}")

    producer.flush() # 모든 메시지 전송 보장
    producer.close()
    print("Finished sending data.")

if __name__ == "__main__":
    send_data_from_file(FILE_PATH)