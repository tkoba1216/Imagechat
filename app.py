from flask import Flask,render_template
from flask_socketio import SocketIO,emit
from datetime import datetime
from pymongo import MongoClient
#from dotenv import load_dotenv
#from python_dotenv import load_dotenv

import os

app = Flask(__name__)

#Socket.ioのセットアップ
socketio = SocketIO(app)


#MongoDBの接続先設定
#load_dotenv()
#mongo_uri = os.environ.get("MONGO_URI")
mongo_uri = "URI"
client = MongoClient(mongo_uri)
db = client["SNS"]
messages_collection = db["messages"]

@app.route("/")
def index():
    return render_template("index.html")

#メッセージの読み込み
@socketio.on("load messages")
def load_messages():
    messages = messages_collection.find().sort("_id",-1).limit(10)
    messages = list(messages)[::-1]
    messages_return = [message["message"] for message in messages]
    #メッセージをクライアントへ送信
    emit("load all messages",messages_return)

#メッセージの登録
@socketio.on("send message")
def send_message(message):
    messages_collection.insert_one({"message":message})
    #メッセージをクライアントへ送信
    emit("load one message",message,broadcast=True)
    

if __name__ == "__main__":
    #Socket.ioサーバの起動
    socketio.run(app,debug=True,port=8000)
