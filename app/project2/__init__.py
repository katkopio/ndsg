from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://admin:azR4ENUNm1FPH4pj@project2.sqrmt.mongodb.net/Project2?retryWrites=true&w=majority"
db = PyMongo(app)

from project2 import routes