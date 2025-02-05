from flask import Flask,render_template
from flask_socketio import SocketIO,emit
from datetime import datetime
from pymongo import MongoClient
#from dotenv import load_dotenv
#from python_dotenv import load_dotenv
import base64
import gridfs
import bson
from bson.objectid import ObjectId

import os

app = Flask(__name__)

#Socket.ioのセットアップ
socketio = SocketIO(app)


#MongoDBの接続先設定
#load_dotenv()
#mongo_uri = os.environ.get("MONGO_URI")
mongo_uri = ""

client = MongoClient(mongo_uri)
db = client["SNS_TEST"]
#messages_collection = db["messages"]

#GridFSのセットアップ
fs = gridfs.GridFS(db)


@app.route("/")
def index():
    return render_template("index.html")

#メッセージの読み込み
@socketio.on("load messages")
def load_messages():
    #表示の数も決めないとこの場合11番目以降の画像でいいねを押せなくなる。
    messages = db.images.find().sort("_id",-1).limit(10)
    messages = list(messages)[::-1]
    #メッセージと画像データをリストにして母えす
    messages_return = [
        {
            "message_id": str(message["_id"]),
            "message": message["message"],
            "emoji": message.get("emoji", "😄"),
            "image_data": get_image_data(message["image_id"]),
            "likes": message.get("likes", 0)  # いいね数がない場合は0
        } 
        for message in messages
    ]
    #メッセージをクライアントへ送信
    emit("load all messages",messages_return)

def get_image_data(image_id):
    image_file = fs.get(image_id).read()
    image_base64 = base64.b64encode(image_file)
    return image_base64.decode("utf-8")

# いいね処理
@socketio.on("like message")
def like_message(data):
    message_id = data["message_id"]
    db.images.update_one({"_id": ObjectId(message_id)}, {"$inc": {"likes": 1}})
    updated_message = db.images.find_one({"_id": ObjectId(message_id)})
    emit("update likes", {"message_id": message_id, "likes": updated_message["likes"]}, broadcast=True)


#メッセージと画像の登録
@socketio.on("send message")
def send_message(data):
    message = data["message"]
    image_data = data["image_data"]
    image_name = data["image_name"]
    emoji = data.get("emoji", "😄")
    
    #bs64エンコードされているデータをデコードしてFridFSに保存
    image_bytes = base64.b64decode(image_data.split(",")[1])
    image_id = fs.put(image_bytes,image_name = image_name)
    
    #MongoDBに画像を保存したGridFSのファイルIDとテキストを保存
    image_record = {
        "image_name": image_name,
        "image_id": image_id,
        "message": message,
        "emoji":emoji,
        "likes": 0  # いいね数を0で初期化
    }
    db.images.insert_one(image_record)
    
    #メッセージと画像をクライアントへ送信
    emit("load one message",{
        "message":message,
        "emoji":emoji,
        "image_data":get_image_data(image_id),"likes":0},broadcast=True)
    #messages_collection.insert_one({"message":message})
    #メッセージをクライアントへ送信
    #emit("load one message",message,broadcast=True)
    

if __name__ == "__main__":
    #Socket.ioサーバの起動
    socketio.run(app,debug=True,port=8000)
