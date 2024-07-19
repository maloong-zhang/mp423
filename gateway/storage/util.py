import pika, json, os


def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
        print(err)
        return f"put file raise error, {str(err)}", 500

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    queue_name = os.environ.get("VIDEO_QUEUE")
    # Check the queue exists or not , if not exists, create it
    # channel.queue_declare(queue=queue_name, durable=False)

    try:
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        print(err)
        fs.delete(fid)
        return f"send message to rabbitmq raise error, {str(err)}", 500
