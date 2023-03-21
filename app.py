from flask import Flask, request
from flask import *
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://OnionPowder01:{password}@cluster0.mzjsypb.mongodb.net/?retryWrites=true&w=majority"  
client = MongoClient(connection_string)
digital_portofolio_db = client.digital_portofolio


@app.route("/publish", methods=["POST"])
def publish():
    collection = digital_portofolio_db.digital
    uid = request.form['uid']
    project_Name = request.form['projectName']
    project_Link = request.form['projectLink']
    project_Image = request.form['projectImage']
    document = {
        "uid": uid,
        "projectName": project_Name,
        "projectLink": project_Link,
        "projectImage": project_Image,
    }
    collection.insert_one(document)
    print(project_Image)
    return "ok"

@app.route("/get-work", methods=["GET"])
def get_work():
    work_list = []
    work_collection = digital_portofolio_db.digital
    work = work_collection.find()
    for elem in work:
        work_list.append(elem)
    return json.loads(json_util.dumps(work_list))

@app.route('/remove')
def remove():
    uid = request.args.get('uid')
    print(uid)
    work_collection = digital_portofolio_db.digital
    work_collection.delete_one({"uid": uid})
    return "file removed"

@app.route("/update", methods=["POST"])
def update():
    collection = digital_portofolio_db.digital
    uid = request.form['uid']
    project_Name = request.form['projectName']
    project_Link = request.form['projectLink']
    project_Image = request.form['projectImage']
    filter = {"uid": uid}
    update = {"$set": {"projectName": project_Name, "projectLink": project_Link, "projectImage": project_Image}}
    collection.update_one(filter, update)
    print(uid)
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)


