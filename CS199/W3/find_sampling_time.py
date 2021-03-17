from pdb import set_trace
import gpxpy.gpx
import datetime

def find_sampling_time(gpx_file_location):
    """
    Calculates sampling time given a GPX file
    """
    points = []
    gpx = gpxpy.parse(gpx_file_location)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(point.time.timestamp())

    summation = 0
    total = len(points) - 1

    for i in range(total):
        summation += points[i+1] - points[i]

    return summation / total

if __name__ == '__main__':
    with open('../DS/ds1.gpx', 'r') as gpx_file_location:
        avg_time = find_sampling_time(gpx_file_location)
    
    print(avg_time)