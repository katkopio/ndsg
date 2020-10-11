import gpxpy
import gpxpy.gpx

def parse_gpx_file(gpx_file_location):
    """
    Parses GPX file to output array of objects
    """
    points = "\"latitude\",\"longitude\",\"time\"\n"
    gpx = gpxpy.parse(gpx_file_location)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points = points + f"{point.latitude},{point.longitude},{point.time}\n"
    return points

def main():
    gpx_file_location = open('../Datasets/ds1_out.gpx', 'r')
    
    gps_data = parse_gpx_file(gpx_file_location)
    print(gps_data)

if __name__ == "__main__":
    main()