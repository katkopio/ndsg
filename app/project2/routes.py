from flask import render_template, url_for, flash, redirect, request
from project2 import app, info
from project2.forms import InputGPXFileForm, SpeedViolationForm, GeofencingForm
from project2.api import parse_gpx_file, distance_travelled, speed_violation, create_geofence
from geojson import Point, Feature

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

def create_geojson_feature(gps_data):
    locations = []
    for location in gps_data:
        point = Point([location['longitude'], location['latitude']])
        feature = Feature(geometry = point)
        locations.append(feature)
    return locations

@app.route("/features/geofencing", methods=['GET','POST'])
def geofencing():
    form = GeofencingForm()
    filename = ""
    locations = []
    results = []
    number_violations = 0
    if request.method == 'POST' and form.validate_on_submit():
        if 'submit' in request.form.to_dict():
            gpx_file = request.files['gpx_file']
            filename = gpx_file.filename
            gps_data = parse_gpx_file(gpx_file)
            locations = create_geojson_feature(gps_data)
        if 'compute' in request.form.to_dict():
            gpx_file = request.files['gpx_file']
            filename = gpx_file.filename
            gps_data = parse_gpx_file(gpx_file)

            lat1 = float(request.form.to_dict().get("lat1"))
            lon1 = float(request.form.to_dict().get("lon1"))
            point1 = (lat1, lon1)
            lat2 = float(request.form.to_dict().get("lat2"))
            lon2 = float(request.form.to_dict().get("lon2"))
            point2 = (lat2, lon2)
            min_time = int(request.form.to_dict().get("min_time"))
            max_time = int(request.form.to_dict().get("max_time"))
            results = create_geofence(gps_data, min_time, max_time, point1, point2)
            number_violations = len(results)
            print(results)
    return render_template('geofencing.html', title='Geofencing', info = info.get("geofencing"), filename=filename, locations=locations, results=results, number_violations=number_violations, form=form)

@app.route("/features/liveness")
def liveness():
    return render_template('liveness.html', title='Liveness', info = info.get("liveness"))

@app.route("/features/route_finding")
def route_finding():
    return render_template('route_finding.html', title='Route Finding', info = info.get("route_finding"))

@app.route("/features/loop_counting")
def loop_counting():
    return render_template('loop_counting.html', title='Loop Counting', info = info.get("loop_counting"))
