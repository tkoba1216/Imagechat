from pymongo import MongoClient
mongo_uri = ""
try:
    client = MongoClient(mongo_uri)
    client.admin.command('ping')  # データベースにpingを送る
    print("MongoDB接続成功")
except Exception as e:
    print(f"MongoDB接続エラー: {e}")