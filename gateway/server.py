import os, gridfs, pika, json, sys
from posix import environ
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId


def create_app():
    server = Flask(__name__)
    videos_uri = "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(
        os.environ.get("MONGO_DB_USERNAME"),
        os.environ.get("MONGO_DB_PASSWORD"),
        os.environ.get("MONGO_DB_HOSTNAME"),
        os.environ.get("MONGO_DB_PORT"),
        os.environ.get("MONGO_VIDEOS_DB"),
    )
    mp3s_uri = "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(
        os.environ.get("MONGO_DB_USERNAME"),
        os.environ.get("MONGO_DB_PASSWORD"),
        os.environ.get("MONGO_DB_HOSTNAME"),
        os.environ.get("MONGO_DB_PORT"),
        os.environ.get("MONGO_MP3S_DB"),
    )

    mongo_video = PyMongo(server, uri=videos_uri)
    mongo_mp3 = PyMongo(server, uri=mp3s_uri)

    video_db = mongo_video.db
    mp3_db = mongo_mp3.db

    try:
        if video_db is None or mp3_db is None:
            print("Video or mp3 db not found")
            sys.exit(1)
        # Try yo access a collection to ensure connection
        video_db.list_collection_names()
        mp3_db.list_collection_names()
    except Exception as e:
        print(f"Error connecting to mongo: {e}")
        sys.exit(1)

    fs_video = gridfs.GridFS(video_db)
    fs_mp3s = gridfs.GridFS(mp3_db)
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()

    @server.route("/login", methods=["POST"])
    def login():
        token, err = access.login(request)
        if not err:
            return str(token)
        else:
            return err

    @server.route("/upload", methods=["POST"])
    def upload():
        access, err = validate.token(request)
        if err or access is None:
            return str(err), 401
        access = json.loads(access)
        if access["admin"]:
            if len(request.files) > 1 or len(request.files) < 1:
                return "exactly 1 file required", 400
            for _, f in request.files.items():
                err = util.upload(f, fs_video, channel, access)
                if err:
                    return err
            return "success", 200
        else:
            return "not authorized", 401

    @server.route("/download", methods=["GET"])
    def download():
        access, err = validate.token(request)

        if err or access is None:
            return err
        access = json.loads(access)

        if access["admin"]:
            fid_string = request.args.get("fid")
            if not fid_string:
                return "fid is required", 400
            try:
                out = fs_mp3s.get(ObjectId(fid_string))
                return send_file(out, download_name=f"{fid_string}.mp3")
            except Exception as err:
                print(err)
                return "internal server error", 500
        return "not authorized", 401

    return server


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
