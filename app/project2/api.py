from haversine import haversine
import gpxpy
import gpxpy.gpx
from shapely.geometry import Point, Polygon
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

def distance_travelled(gps_data):
    """
    Calculates total distance travelled in km
    """
    distance_travelled = 0.0
    for i in range(len(gps_data) - 1):
        distance_travelled += haversine((gps_data[i].get('latitude'), gps_data[i].get('longitude')), 
            (gps_data[i+1].get('latitude'), gps_data[i+1].get('longitude')))
    
    return '%.4f'%(distance_travelled)

def sec_to_minute(seconds):
    return seconds / 60.0

def sec_to_hour(seconds):
    return seconds / 3600.0

def speed_between_points(lon1, lat1, time1, lon2, lat2, time2):
    """
    Given 2 GPS points, calculate the speed between them
    """
    d_time = sec_to_hour(time2.timestamp() - time1.timestamp())
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
            time_elapsed += time1.timestamp() - time0.timestamp()

            if (first_point == True):
                starting_point = gps_data[i]
                first_point = False

        else:
            speeding = False

            if (sec_to_minute(time_elapsed) >= time): 
                list_violations.append((time_elapsed, starting_point, gps_data[i-1]))

            time_elapsed = -1
            first_point = True

    return list_violations

def stop_violation(gps_data, min_limit, max_time, point1, point2):
    fence = Polygon([point1, (point1[0], point2[1]), point2, (point2[0], point1[1])])
    index_start = -1
    results = []

    for i in range(len(gps_data)):
        pt = Point(gps_data[i].get('latitude'), gps_data[i].get('longitude'))

        if fence.intersects(pt):
            if index_start == -1:
                index_start = i
        else:
            if index_start != -1:
                timer_start = gps_data[index_start].get('time').timestamp()
                timer_end = gps_data[i-1].get('time').timestamp()
                fence_time = timer_end - timer_start

                if fence_time < min_limit:
                    results.append({
                        'violation': 'below limit',
                        'time': fence_time,
                        'start': gps_data[index_start].get('time').strftime('%X'),
                        'end': gps_data[i-1].get('time').strftime('%X')
                    })
                elif fence_time > max_time:
                    results.append({
                        'violation': 'above limit',
                        'time': fence_time,
                        'start': gps_data[index_start].get('time').strftime('%X'),
                        'end': gps_data[i-1].get('time').strftime('%X')
                    })
                
                index_start = -1

    return results

def check_liveness(gps_data, time_limit):
    """
    Determines total "aliveness" time of a vehicle. The
    vehicle is considered "alive" if the gaps between
    GPS readings are less than given {time_limit}.
    Input:  gps_data (array of dictionaries)
            time_limit (in seconds)
    Output: total_liveness (in seconds)
            results (array of dictionaries)
    """
    results = []
    total_liveness = 0
    start_index = 0

    for i in range(len(gps_data) - 1):
        time0 = gps_data[i].get("time")
        time1 = gps_data[i+1].get("time")
        time_diff = time1.timestamp() - time0.timestamp()

        if time_diff >= time_limit:
            segment_liveness = time0.timestamp() - gps_data[start_index].get("time").timestamp()
            results.append({
                "liveness": segment_liveness,
                "start": gps_data[start_index].get("time"),
                "end": gps_data[i].get("time")
            })
            start_index = i + 1
            total_liveness += segment_liveness
    
    time0 = gps_data[start_index].get("time")
    time1 = gps_data[-1].get("time")
    segment_liveness = time1.timestamp() - time0.timestamp()
    results.append({
        "liveness": segment_liveness,
        "start": time0,
        "end": time1
    })
    total_liveness += segment_liveness

    return total_liveness, results
