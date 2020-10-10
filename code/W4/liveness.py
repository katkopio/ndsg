import gpxpy
import gpxpy.gpx
import sys

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

def liveness(gps_data, time_limit):
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

def main(time_limit):
    # gpx_file_location = open("../Datasets/ds1_out.gpx", "r")
    # gpx_file_location = open("../Datasets/20200924.gpx", "r")
    gpx_file_location = open("../Datasets/Laramie_Enduro_2014..gpx", "r")

    gps_data = parse_gpx_file(gpx_file_location)
    total_liveness, results = liveness(gps_data, time_limit)

    print(f"Total Liveness: {total_liveness}\n")
    for result in results:
        print(f"segment liveness: {result.get('liveness')}")
        print(f"start: {result.get('start').strftime('%X')}")
        print(f"end: {result.get('end').strftime('%X')}\n")

if __name__ == "__main__":
    main(int(sys.argv[1]))