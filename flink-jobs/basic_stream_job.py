# flink-jobs/basic_stream_job.py

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.common.typeinfo import Types

def basic_streaming_job():
    # 1. 스트림 실행 환경 설정
    env = StreamExecutionEnvironment.get_execution_environment()
    # Flink Kafka 커넥터 jar 파일 추가. docker-compose에서 마운트한 경로를 사용
    env.add_jars("file:///opt/flink/usrlib/flink-sql-connector-kafka-3.1.0-1.18.jar")

    # 2. 카프카 소스(Source) 정의
    # 데이터가 흘러 들어오는 입구를 설정합니다.
    kafka_source = FlinkKafkaConsumer(
        topics='user-behavior',
        deserialization_schema=JsonRowDeserializationSchema.builder()
            .type_info(Types.ROW([
                Types.STRING(),
                Types.STRING(),
                Types.STRING(),
                Types.FLOAT(),
                Types.STRING()
            ])).build(),
        properties={
            'bootstrap.servers': 'kafka1:9092,kafka2:9092,kafka3:9092', # Docker 내부 네트워크에서 사용하는 주소
            'group.id': 'flink-group-1'
        }
    )

    # 3. 데이터 스트림 생성
    # 카프카 소스로부터 데이터를 읽어 스트림을 만듭니다.
    data_stream = env.add_source(kafka_source, "Kafka Source")

    # 4. 데이터 처리 및 출력(Sink)
    # 지금은 가장 간단한 처리인 '출력'을 합니다.
    data_stream.print()

    # 5. 작업 실행
    env.execute("Basic Kafka to Console Job")

if __name__ == '__main__':
    basic_streaming_job()