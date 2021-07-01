from numpy import array, mean, std, ceil
import datetime, gpxpy.gpx

def find_time_diff(gpx_file_location):
    """
    Calculates sampling time given a GPX file
    """
    points = []
    gpx = gpxpy.parse(gpx_file_location)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(point.time.timestamp())

    time_diff = []
    total = len(points) - 1

    for i in range(total):
        time_diff.append(points[i+1] - points[i])

    return time_diff

def find_sampling_time(data):
    avg = mean(data)
    sd = std(data)
    return avg, sd

def reject_outliers(data, m=2):
    return data[abs(data - mean(data)) < m * std(data)]

def generate_data():
    filenames = ['DS7-1-0420', 'DS7-2-0421', 'DS7-3-0422', 'DS7-4-0424', 'DS7-5-0425', 'DS7-6-0426', 'ds1']
    a = []
    for file in filenames:
        with open(f'../../DS/{file}.gpx', 'r') as gpx_file_location:
            time_diff = find_time_diff(gpx_file_location)

        data = reject_outliers(array(time_diff))
        avg, sd = find_sampling_time(data)
        print(ceil(avg+sd))

if __name__ == '__main__':
    # with open('../../DS/DS7-1-0420.gpx', 'r') as gpx_file_location:
    #     time_diff = find_time_diff(gpx_file_location)

    # data = reject_outliers(array(time_diff))
    # avg, sd = find_sampling_time(data)

    # print(f"Samples a point every {avg} seconds pm {sd}")
    generate_data()