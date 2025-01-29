from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDBに接続
def test_db_connection():
    mongo_uri = ""  # 実際のMongoDB URIに置き換える
    client = MongoClient(mongo_uri)
    db = client["SNS_IMG"]
    
    # 適当なデータを取得
    sample_data = db.images.find_one()
    if sample_data:
        _id = sample_data["_id"]
        print(f"Test _id: {_id}")
        
        # _id を指定して image_name を取得
        result = db.images.find_one({"_id": ObjectId(_id)})
        if result:
            print(f"Image Name: {result['image_name']}")
            
            # image_name を変更
            #new_name = "updated_image_name.jpg"
            #db.images.update_one({"_id": ObjectId(_id)}, {"$set": {"image_name": new_name}})
            #print(f"Updated Image Name to: {new_name}")
            print(f"like is pushed!")
            # いいね（like）の追加テスト
            if "like" not in result:
                db.images.update_one({"_id": ObjectId(_id)}, {"$set": {"like": 0}})
            else:db.images.update_one({"_id": ObjectId(_id)}, {"$inc": {"like": 1}})
                
            
            # いいねを増やす
            #db.images.update_one({"_id": ObjectId(_id)}, {"$inc": {"like": 1}})
            
            # 更新後のデータを取得
            #updated_result = db.images.find_one({"_id": ObjectId(_id)})
            #print(f"Updated Like Count: {updated_result['like']}")
        else:
            print("No matching document found.")
    else:
        print("No data found in collection.")

if __name__ == "__main__":
    test_db_connection()