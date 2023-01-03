import torch
import crawler

from kafka import KafkaConsumer
from json import loads

# 카프카 서버
bootstrap_servers = ["host.docker.internal:9092"]

# 카프카 토픽
str_topic_name    = 'Topic3'

# 카프카 소비자 group1 생성
str_group_name = 'group1'
consumer = KafkaConsumer(str_topic_name, bootstrap_servers=bootstrap_servers,
                         auto_offset_reset='earliest', # 가장 처음부터 소비
                         enable_auto_commit=True,
                         group_id=str_group_name,
                         value_deserializer=lambda x: loads(x.decode('utf-8')),                       
                         consumer_timeout_ms=60000 # 타임아웃지정(단위:밀리초)
                        )


if __name__ == "__main__":
    
    for message in consumer:
        image_nums = message.value['image_nums']
        keywords = message.value['keywords']
        print(message)
        custom_crawler = crawler.GoogleImageCrawler(
            maximum_image_count = message.value['image_nums'])
        custom_crawler.search(message.value['keywords'])
    
    