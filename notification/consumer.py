import pika, sys, os, time
from send import email


def main():
    # rabbitmq connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = email.notification(body)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    queue_name = os.environ.get("MP3_QUEUE")
    # Check the queue exists or not , if not exists, create it
    # channel.queue_declare(queue=queue_name, durable=False)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("Waiting for messages. To exit press CTRL+C")

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
