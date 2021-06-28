import gpxpy 
import datetime

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

def write_gpx_file(files, interval):
    with open('traj_points/nsweep_1000.gpx','r') as gpx_file:
        gps_data = gpxpy.parse(gpx_file)

        for i in range(files):
            gpx = gpxpy.gpx.GPX()

            gpx_track = gpxpy.gpx.GPXTrack()
            gpx.tracks.append(gpx_track)

            gpx_segment = gpxpy.gpx.GPXTrackSegment()
            gpx_track.segments.append(gpx_segment)

            segment = gps_data.tracks[0].segments[0]
            counter = 0
            for j in range(int((i + 1) * interval / 100 + 1)):
                for point in segment.points:
                    lat = point.latitude
                    lon = point.longitude
                    time = point.time.timestamp()
                    time += 86400 * j
                    time = datetime.datetime.fromtimestamp(time)
                    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, time=time))
                    counter += 1
            print(counter)
            with open(f'traj_points/nsweep_{(i+1) * interval + 1000}.gpx','w') as f:
                f.write(gpx.to_xml())

if __name__ == "__main__":
    files = 10
    interval = 10000

    write_gpx_file(files, interval)