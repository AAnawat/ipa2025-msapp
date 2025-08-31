from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGO_URI)
database = client[DB_NAME]
collection = database["router-informaion"]

@app.route("/")
def main():
    data = collection.find()
    return render_template("index.html", data=data)

@app.route('/add', methods=['POST'])
def add_router():
    ip = request.form.get("IP")
    username = request.form.get("username")
    password = request.form.get("password")

    if (ip and username and password):
        collection.insert_one({
            "ip": ip,
            "username": username,
            "password": password
        })
    return redirect("/")

@app.route('/delete', methods=['POST'])
def delete_router():
    data = collection.find()

    try:
        idx = request.form.get("idx")
        query = {"_id": ObjectId(idx)}
        collection.delete_one(query)
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

