from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import WatermarkStrategy, Types
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.datastream.formats.json import JsonRowDeserializationSchema

def basic_streaming_job():
    # 1. 실행 환경
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    # 필드 이름과 타입을 각각의 리스트로 정의
    field_names = ['user_id', 'product_id', 'event_type', 'price', 'event_time']
    field_types = [Types.STRING(), Types.STRING(), Types.STRING(), Types.FLOAT(), Types.STRING()]

    # 2. Kafka Source 정의
    deser = JsonRowDeserializationSchema.builder() \
        .type_info(
            # 핵심 수정사항: Types.ROW_NAMED에 이름 리스트와 타입 리스트를 전달
            Types.ROW_NAMED(field_names, field_types)
        ).build()

    source = KafkaSource.builder() \
        .set_bootstrap_servers("kafka1:9092,kafka2:9092,kafka3:9092") \
        .set_topics("test") \
        .set_group_id("flink-group-1") \
        .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
        .set_value_only_deserializer(deser) \
        .build()

    # 3. 데이터 스트림 생성
    data_stream = env.from_source(
        source,
        WatermarkStrategy.no_watermarks(),
        "Kafka Source"
    )

    # 4. 처리 및 출력
    data_stream.print()

    # 5. 실행
    env.execute("Basic Kafka to Console Job")

if __name__ == "__main__":
    basic_streaming_job()
