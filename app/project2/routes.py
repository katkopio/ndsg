from flask import render_template, url_for, flash, redirect, request
from project2 import app, db, info
# from project2.forms import 
# from project2.models import 

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/features")
def features():
    return render_template('features.html', title='Features', info = info.items())

@app.route("/features/total_distance")
def total_distance():
    return render_template('total_distance.html', title='Total Distance', info = info.get("total_distance"))

@app.route("/features/speeding")
def speeding():
    return render_template('speeding.html', title='Speeding', info = info.get("speeding"))

@app.route("/geofencing")
def geofencing():
    return render_template('geofencing.html', title='Geofencing', info = info.get("geofencing"))

@app.route("/liveness")
def liveness():
    return render_template('liveness.html', title='Liveness', info = info.get("liveness"))

@app.route("/route_finding")
def route_finding():
    return render_template('route_finding.html', title='Route Finding', info = info.get("route_finding"))

@app.route("/loop_counting")
def loop_counting():
    return render_template('loop_counting.html', title='Loop Counting', info = info.get("loop_counting"))
