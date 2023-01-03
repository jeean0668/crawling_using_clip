from kafka import KafkaProducer
from json import dumps
import time

from kafka import KafkaProducer
from json import dumps
import time

def on_send_success(record_metadata):
    # 보낸데이터의 매타데이터를 출력한다
    print("record_metadata:", record_metadata)
    
# 카프카 서버
bootstrap_servers = ["host.docker.internal:9092"]

# 카프카 공급자 생성
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         key_serializer=None,
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

# 카프카 토픽
str_topic_name1 = 'Topic1'
str_topic_name2 = 'Topic2'
str_topic_name3 = 'Topic3'

# 카프카 공급자 토픽에 데이터를 보낸다
data1 = {"time": time.time(), 
        'keywords' : 'dark cloud images',
        'image_nums' : 1000}

data2 = {"time": time.time(), 
        'keywords' : 'dark cloud drawing',
        'image_nums' : 1000}

data3 = {"time": time.time(), 
        'keywords' : 'dark cloud games',
        'image_nums' : 1000}

producer.send(str_topic_name1, value=data1).add_callback(on_send_success)\
                                         .get(timeout=100) # blocking maximum timeout

producer.send(str_topic_name2, value=data2).add_callback(on_send_success)\
                                         .get(timeout=100) 
producer.send(str_topic_name3, value=data3).add_callback(on_send_success)\
                                         .get(timeout=100) 
print('data1:', data1)
print('data2:', data2)
print('data3:', data3)