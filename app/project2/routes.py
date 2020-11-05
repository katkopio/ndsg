from flask import render_template, url_for, flash, redirect, request
from project2 import app, info
from project2.forms import InputGPXFileForm, SpeedViolationForm
from project2.api import parse_gpx_file, distance_travelled, speed_violation

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/features")
def features():
    return render_template('features.html', title='Features', info = info.items())

@app.route("/features/total_distance", methods=['GET','POST'])
def total_distance():
    form = InputGPXFileForm()
    filename = ""
    distance = None
    if request.method == 'POST' and form.validate_on_submit():
        gpx_file = request.files['gpx_file']
        filename = gpx_file.filename
        gps_data = parse_gpx_file(gpx_file)
        distance = distance_travelled(gps_data)
    return render_template('total_distance.html', title='Total Distance', info = info.get("total_distance"), filename=filename, distance=distance, form=form)

@app.route("/features/speeding", methods=['GET','POST'])
def speeding():
    form = SpeedViolationForm()
    filename = ""
    violations = ""
    number_violations = 0
    if request.method == 'POST' and form.validate_on_submit():
        speed_limit = form.speed_limit.data
        time = form.time_minutes.data
        gpx_file = request.files['gpx_file']
        filename = gpx_file.filename
        gps_data = parse_gpx_file(gpx_file)
        violations = speed_violation(gps_data, "Location", speed_limit, time)
        number_violations = len(violations)
    return render_template('speeding.html', title='Speeding', info = info.get("speeding"), filename=filename, violations=violations, number_violations = number_violations, form=form)

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
