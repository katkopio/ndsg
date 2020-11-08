import os
from flask import Flask
from project2.config import Config 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

info = {
    "total_distance": [
        "Total Distance Travelled", 
        "Uses the Haversine formula to calculate the total distance travelled given a GPX file.",
        "It was the first Nelvana-produced series to air on PBS before the Bookworm Bunch and Cyberchase. In 2017, on the 20th anniversary of the series' cancellation, a sequel series titled The Magic School Bus Rides Again premiered on Netflix."],
    "speeding": [
        "Speeding Violation Detector", 
        "Determines if a speeding violation (in km/hr) occured for a given duration of time (in minutes). This can detect speeding in 2 ways: from the speed readings in the GPX file ('Explicit'), or by calcuating the speed from the latitude and longitude ('Location').",
        "Miss Frizzle embarks on adventures with her class on the eponymous school bus. As they journey on their exciting field trips, they discover locations, creatures, time periods and more to learn about the wonders of science along the way."],
    "stop": [
        "Stop Violation Detector", 
        "Determines if a stop violation occured. A vehicle is only allowed to stay in a given location for a defined duration of time. The user must input the upper left and lower right points of the location, and the minimum and maximum allowed time.",
        "In 1994, The Magic School Bus concept was made into an animated series of the same name by Scholastic Entertainment and it premiered on September 10, 1994. The idea for the TV series was developed by former Scholastic Entertainment Vice President and Senior Editorial Director Craig Walker."],
    "liveness": [
        "Liveness Checking", 
        "Determines the total time a vehicle is \"alive\" or active. A vehicle is considered alive if the gaps between GPS readings are less than a given time limit",
        "Scholastic Entertainment president Deborah Forte explained that adapting the books into an animated series was an opportunity to help kids \"learn about science in a fun way\".During this time, Forte had been hearing concerns from parents and teachers about how to improve science education for kids and minorities across the globe."],
    "loop_counting": [
        "Loop Counter", 
        "Calculates the number of loops a vehicle makes in a route, given a grid size in km",
        "Within the episodes, there were also time points where the episode fades out and then fades back in after a series of commercials are shown. On non-commercial networks, VHS, and DVD releases the scene immediately fades back in right after it fades out as no commercials are shown."]
}

from project2 import routes