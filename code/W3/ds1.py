from haversine import haversine
import gpxpy
import gpxpy.gpx

import pdb

def parse_gpx_file(gpx_file_location):
    """
    Parses GPX file to output array of objects
    """
    points = []
    gpx = gpxpy.parse(gpx_file_location)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation,
                    'time': point.time,
                    'speed': point.speed
                })
    unique_points = list({point['time']:point for point in points}.values())

    return unique_points

def total_distance(gps_data):
    """
    Calculates total distance travelled in km
    """
    distance_travelled = 0.0
    for i in range(len(gps_data) - 1):
        distance_travelled += haversine((gps_data[i].get('latitude'), gps_data[i].get('longitude')), 
            (gps_data[i+1].get('latitude'), gps_data[i+1].get('longitude')))

    return distance_travelled

def sec_to_minute(seconds):
    return seconds / 60.0

def sec_to_hour(seconds):
    return seconds / 3600.0

def speed_between_points(lon1, lat1, time1, lon2, lat2, time2):
    """
    Given 2 GPS points, calculate the speed between them
    """
    d_time = sec_to_hour((time2 - time1).seconds)
    d_distance = haversine((lat1, lon1), (lat2, lon2))
    return d_distance / d_time

def speed_violation(gps_data, type, speed_limit, time):
    """
    Determines if a speed violation of {speed_limit}
    occured for {time} minutes, given {type} of analysis.
    Input:
        type = "Explicit" or "Location"
        speed_limit in km/hr
        time in minutes
    """
    time_elapsed = -1
    first_point = True
    list_violations = []
    for i in range(len(gps_data) - 1):
        time0 = gps_data[i-1].get("time")
        lon1 = gps_data[i].get("longitude")
        lat1 = gps_data[i].get("latitude")
        time1 = gps_data[i].get("time")
        lon2 = gps_data[i+1].get("longitude")
        lat2 = gps_data[i+1].get("latitude")
        time2 = gps_data[i+1].get("time")

        if type == "Explicit":
            if(gps_data[i].get("speed") is None):
                speed = speed_between_points(lon1, lat1, time1, lon2, lat2, time2)
            else:
                speed = gps_data[i].get("speed")
        elif type == "Location":
            speed = speed_between_points(lon1, lat1, time1, lon2, lat2, time2)

        if(speed >= speed_limit):
            speeding = True
            time_elapsed += (time1 - time0).seconds

            if (first_point == True):
                starting_point = gps_data[i]
                first_point = False

        else:
            speeding = False

            if (sec_to_minute(time_elapsed) >= time): 
                list_violations.append((sec_to_minute(time_elapsed), starting_point, gps_data[i-1]))

            time_elapsed = -1
            first_point = True

    return list_violations

def main():
    # gpx_file_location = open('datasets/ds1.gpx', 'r')
    gpx_file_location = open('datasets/ds2.gpx', 'r')

    gps_data = parse_gpx_file(gpx_file_location)
    distance = total_distance(gps_data)
    violations = speed_violation(gps_data, "Location", 20.0, 1.0)

    print(f"Total Distance Travelled: {distance}")
    print("---------------------------------------")

    print(f"Violations:")
    for violation in violations:
        print(f"Time: {violation[0]} minutes")
        print(f"Lat1: {violation[1].get('latitude')}")
        print(f"Lon1: {violation[1].get('longitude')}")
        print(f"Time1: {violation[1].get('time')}")
        print(f"Lat2: {violation[2].get('latitude')}")
        print(f"Lon2: {violation[2].get('longitude')}")
        print(f"Time2: {violation[2].get('time')}")
        print("---------------------------------------")

if __name__ == "__main__":
    main()