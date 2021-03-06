from flask import render_template, url_for, flash, redirect, request
from project2 import app, info
from project2.forms import InputGPXFileForm, SpeedViolationForm, StopViolationForm, LivenessForm, LoopForm
from project2.api import parse_gpx_file, distance_travelled, speed_violation, stop_violation, check_liveness, generate_corner_pts, generate_grid_pts, generate_grid_fence, generate_path, generate_route, route_check
from geojson import Point, Feature

ALLOWED_EXTENSIONS = {'gpx'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    return render_template('total_distance.html', title='Total Distance Calculator', info = info.get("total_distance"), filename=filename, distance=distance, form=form)

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
    return render_template('speeding.html', title='Speeding Violation Detection', info = info.get("speeding"), filename=filename, violations=violations, number_violations = number_violations, form=form)

def create_geojson_feature(gps_data):
    locations = []
    for location in gps_data:
        point = Point([location['longitude'], location['latitude']])
        feature = Feature(geometry = point)
        locations.append(feature)
    return locations

@app.route("/features/stop", methods=['GET','POST'])
def stop():
    form = StopViolationForm()
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
            results = stop_violation(gps_data, min_time, max_time, point1, point2)
            number_violations = len(results)
            print(results)
    return render_template('stop_violation.html', title='Stop Violation Detection', info = info.get("stop"), filename=filename, locations=locations, results=results, number_violations=number_violations, form=form)

@app.route("/features/liveness", methods=['GET','POST'])
def liveness():
    form = LivenessForm()
    filename = ""
    total_liveness = -1
    results = []
    if request.method == 'POST' and form.validate_on_submit():
        time_limit = form.time_limit.data
        gpx_file = request.files['gpx_file']
        filename = gpx_file.filename
        gps_data = parse_gpx_file(gpx_file)
        total_liveness, results = check_liveness(gps_data,time_limit)
    return render_template('liveness.html', title='Liveness Checking', info = info.get("liveness"), filename=filename, total_liveness=total_liveness, results=results, form=form)

@app.route("/features/loop_counting", methods=['GET','POST'])
def loop_counting():
    form = LoopForm()
    filename = ""
    loops = -1
    if request.method == 'POST' and form.validate_on_submit():
        side_length = form.side_length.data 
        gpx_file = request.files['gpx_file']
        filename = gpx_file.filename 

        gps_data = parse_gpx_file(gpx_file)
        point1, point2 = generate_corner_pts(gps_data)
        grid_pts = generate_grid_pts(point1, point2, side_length)
        grid_fence = generate_grid_fence(grid_pts)
        vehicle_route = generate_path(gps_data, grid_fence)
        set_route = generate_route(vehicle_route)
        loops = route_check(set_route, vehicle_route)
    return render_template('loop_counting.html', title='Loop Counting', info = info.get("loop_counting"), filename=filename, loops=loops, form=form)

# import os
# import uuid
# from project2.models import GPXFile
# from werkzeug.utils import secure_filename

# Code to save to DB and save file
        # if gpx_file and allowed_file(filename):
        #     # Calculations
        #     # Save File
        #     saved_file = str(uuid.uuid4().hex)
        #     gpx_file.save(os.path.join(app.config['UPLOAD_FOLDER'], saved_file))
        #     # Save to DB
        #     gpx_db = GPXFile(file_name=saved_file)
        #     db.session.add(gpx_db)
        #     db.session.commit()