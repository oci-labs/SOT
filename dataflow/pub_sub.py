from google.cloud import pubsub_v1
import time
import json

project_id = 'securityofthings'
topic_name = 'mk_topic'

credentials = 'dataflow/service_account_key.json'
publisher = pubsub_v1.PublisherClient()  # credentials=credentials)

topic_path = publisher.topic_path(project_id, topic_name)

if __name__ == '__main__':
    def callback(message_future):
        # When timeout is unspecified, the exception method waits indefinitely.
        if message_future.exception(timeout=30):
            print('Publishing message on {} threw an Exception {}.'.format(
                topic_name, message_future.exception()))
        else:
            print(message_future.result())


    for n in range(10000):
        data = {'mk': 'Message'}  #.format(n)
        data = json.dumps(data)
        # data = str.encode(data)
        # Data must be a bytestring
        # data = data.encode('utf-8')
        # When you publish a message, the client returns a Future.
        message_future = publisher.publish(topic_path, data=data)
        message_future.add_done_callback(callback)
        time.sleep(1)
        print('Published message IDs:{}'.format(n))
