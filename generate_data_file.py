import json
import random
from datetime import datetime
from faker import Faker
from tqdm import tqdm
import os

fake = Faker()

def generate_log_entry():
    """하나의 로그 데이터(JSON)를 생성하는 함수"""
    event_type = random.choice(['click', 'add_to_cart', 'purchase'])
    price = round(random.uniform(10.0, 500.0), 2) if event_type == 'purchase' else None
    return {
        'user_id': fake.uuid4(),
        'product_id': f'product_{random.randint(1,1000)}',
        'event_type': event_type,
        'price': price,
        'event_time': datetime.now().isoformat()
    }

def create_dummy_data_file(filename="dummy_data.json", target_size_gb=10):
    """지정한 크기의 더미 데이터 파일을 생성하는 함수"""
    target_size_bytes = target_size_gb * 1024 * 1024 * 1024
    print(f"{target_size_gb}GB의 {filename} 생성 중...")

    with open(filename, 'w') as f:
        # tqdm으로 진행률 표시
            with tqdm(total=target_size_gb, unit='8', unit_scale=True, desc="데이터 생성 중...") as pbar:
                 while os.path.getsize(filename) < target_size_bytes:
                      log_entry = generate_log_entry()
                      json_str = json.dumps(log_entry) + '\n' # JSONL 형식 
                      f.write(json_str)
                      pbar.update(len(json_str.encode('utf-8')))

    print(f"{os.path.getsize(filename) / (1024**3):.2f} GB의 {filename} 파일 생성 성공")

if __name__ == "__main__":
     create_dummy_data_file("test_dummy_data.json",1)
