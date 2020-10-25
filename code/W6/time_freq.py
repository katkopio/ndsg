import gpxpy
import sys

def time_freq(time_diff):
    gpx = gpxpy.gpx.GPX()

    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    
    with open('ds1_times/base.gpx','r') as gpx_file:
        gpx_vehicle = gpxpy.parse(gpx_file)

        segment = gpx_vehicle.tracks[0].segments[0]
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(segment.points[0].latitude, segment.points[0].longitude, time=segment.points[0].time))
        current_point_time = segment.points[0].time.timestamp()

        for point in segment.points:
            if point.time.timestamp() - current_point_time >= time_diff:
                gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point.latitude, point.longitude, time=point.time))
                current_point_time = point.time.timestamp()
    
    file_name = 'ds1_times/ds1_time_' + str(time_diff) + 's.gpx'

    with open(file_name, 'w') as f:
        f.write(gpx.to_xml())

if __name__ == '__main__':
    time_freq(int(sys.argv[1]))

# to run use 'python time_freq.py <time interval between gps logs in seconds>'
# Given interval, chops up base.gpx file
# Input ds1_times/base.gpx
# Output ds1_times/ds1_time_<time>s.gpx