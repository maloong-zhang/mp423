import pika, sys, os
from pymongo import MongoClient
import gridfs
from convert import to_mp3


def main():
    port = os.environ.get("MONGO_PORT")
    if port is None:
        port = 27017
    port = int(port)
    client = MongoClient(
        host=os.environ.get("MONGO_HOST"),
        port=port,
        username=os.environ.get("MONGO_DB_USERNAME"),
        password=os.environ.get("MONGO_DB_PASSWORD"),
        authSource="admin",
    )
    db_videos = client.videos
    db_mp3s = client.mp3s

    # gridfs
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    # rabbitmq connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    queue_name = os.environ.get("VIDEO_QUEUE")
    # Check the queue exists or not , if not exists, create it
    # channel.queue_declare(queue=queue_name, durable=False)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
    )
    print("Waiting for messages, To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
