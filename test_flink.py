# word_count.py

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.typeinfo import Types

def word_count_job():
    # 1. 실행 환경 생성
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1) # 병렬성을 1로 설정하여 출력 순서 보장

    # 2. Source: Python 리스트로부터 데이터 스트림 생성
    data_stream = env.from_collection(
        collection=[
            (1, 'Hello Flink'),
            (2, 'Hello PyFlink')
        ],
        type_info=Types.TUPLE([Types.INT(), Types.STRING()])
    )

    # 3. Transformation: 들어온 문장을 단어로 분리하고 (단어, 1) 형태로 변환
    # flat_map: 1개의 입력을 N개의 출력으로 만들 수 있음
    word_count_stream = data_stream \
        .flat_map(lambda x: [(word, 1) for word in x[1].split()]) \
        .key_by(lambda x: x[0]) \
        .sum(1)

    # 4. Sink: 결과물을 콘솔에 출력
    word_count_stream.print()

    # 5. 잡(Job) 실행
    env.execute("Word Count Example")

if __name__ == '__main__':
    word_count_job()