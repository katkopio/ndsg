import os
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SECRET_KEY'] = '824fb3bf0f538824c22fe8b8e26a2596'
app.config["MONGO_URI"] = "mongodb+srv://admin:azR4ENUNm1FPH4pj@project2.sqrmt.mongodb.net/Project2?retryWrites=true&w=majority"
mongo = PyMongo(app)

info = {
    "total_distance": [
        "Total Distance Travelled", 
        # "Uses the Haversine formula to calculate the total distance travelled given a GPX file.",
        "It was the first Nelvana-produced series to air on PBS before the Bookworm Bunch and Cyberchase. In 2017, on the 20th anniversary of the series' cancellation, a sequel series titled The Magic School Bus Rides Again premiered on Netflix."],
    "speeding": [
        "Speeding Violation Detector", 
        "Miss Frizzle embarks on adventures with her class on the eponymous school bus. As they journey on their exciting field trips, they discover locations, creatures, time periods and more to learn about the wonders of science along the way."],
    "geofencing": [
        "Geofence Creation", 
        "In 1994, The Magic School Bus concept was made into an animated series of the same name by Scholastic Entertainment and it premiered on September 10, 1994. The idea for the TV series was developed by former Scholastic Entertainment Vice President and Senior Editorial Director Craig Walker."],
    "liveness": [
        "Liveness Checking", 
        "Scholastic Entertainment president Deborah Forte explained that adapting the books into an animated series was an opportunity to help kids \"learn about science in a fun way\".During this time, Forte had been hearing concerns from parents and teachers about how to improve science education for kids and minorities across the globe."],
    "route_finding": [
        "Route Finding", 
        "When The Magic School Bus was syndicated on commercial networks, the Producer Says segment at the end of each episode was cut out to make space for commercials. The Producer Says segments were only seen when the series was shown on non-commercial networks, international networks, VHS, and DVD releases."],
    "loop_counting": [
        "Loop Counter", 
        "Within the episodes, there were also time points where the episode fades out and then fades back in after a series of commercials are shown. On non-commercial networks, VHS, and DVD releases the scene immediately fades back in right after it fades out as no commercials are shown."]
}

from project2 import routes