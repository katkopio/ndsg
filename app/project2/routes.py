from flask import render_template, url_for, flash, redirect, request
from project2 import app, db
# from project2.forms import 
# from project2.models import 

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')
