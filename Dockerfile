FROM flink:1.18.0-scala_2.12-java11

USER root

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip openjdk-11-jdk && \
    rm -rf /var/lib/apt/lists/*

    # (가장 중요) JAVA_HOME을 새로 설치한 JDK 경로로 설정
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

RUN ln -s /usr/bin/python3 /usr/bin/python

# Kafka DataStream 커넥터
RUN curl -fsSL \
  https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/3.2.0-1.18/flink-connector-kafka-3.2.0-1.18.jar \
  -o /opt/flink/lib/flink-connector-kafka-3.2.0-1.18.jar

# Kafka Client Library (필수)
RUN curl -fsSL \
  https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.0/kafka-clients-3.4.0.jar \
  -o /opt/flink/lib/kafka-clients-3.4.0.jar

# (선택) Redis Sink - Apache Bahir (보수 중단, 호환성 이슈 시 Python 클라이언트 사용 권장)
RUN curl -fsSL \
  https://repo1.maven.org/maven2/org/apache/bahir/flink-connector-redis_2.12/1.1.0/flink-connector-redis_2.12-1.1.0.jar \
  -o /opt/flink/lib/flink-connector-redis_2.12-1.1.0.jar

# Bahir가 의존하는 Jedis
RUN curl -fsSL \
  https://repo1.maven.org/maven2/redis/clients/jedis/2.9.0/jedis-2.9.0.jar \
  -o /opt/flink/lib/jedis-2.9.0.jar

COPY flink-jobs/requirements.txt /tmp/requirements.txt
# JDK 경로를 동적으로 찾아서 JAVA_HOME으로 설정한 뒤 pip install 실행
RUN export JAVA_HOME=$(find /usr/lib/jvm -name "javac" | sed "s|/bin/javac||") && \
    pip install --no-cache-dir -r /tmp/requirements.txt

USER flink


