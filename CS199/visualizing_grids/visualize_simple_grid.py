from api import parse_gpx_file
from grid_creation import create_simple_gridmap
import gpxpy

def visualize_fences(grid_fence, side_length, filename):
    gpx = gpxpy.gpx.GPX()

    for i in range(len(grid_fence)):
        for j in range(len(grid_fence[0])):
            top_left_pt = gpxpy.gpx.GPXWaypoint()
            top_left_pt.latitude = grid_fence[i][j].top_left_pt.lat
            top_left_pt.longitude = grid_fence[i][j].top_left_pt.lon

            bottom_right_pt = gpxpy.gpx.GPXWaypoint()
            bottom_right_pt.latitude = grid_fence[i][j].bottom_right_pt.lat
            bottom_right_pt.longitude = grid_fence[i][j].bottom_right_pt.lon

            gpx.waypoints.append(top_left_pt)
            gpx.waypoints.append(bottom_right_pt)

    with open(f'../DS/{filename}.gpx', 'r') as gpx_file:
        gpx_vehicle = gpxpy.parse(gpx_file)

        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        segment = gpx_vehicle.tracks[0].segments[0]
        for point in segment.points:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point.latitude, point.longitude, time=point.time))

    grid_size = str(side_length) + 'km'
    file_name = f'DS2_0420/ds2_0420_{grid_size}.gpx'

    with open(file_name, 'w') as f:
        f.write(gpx.to_xml())

if __name__ == '__main__':
    # Open Files
    filename = "DS7-1-0420"
    with open(f'../DS/{filename}.gpx', 'r') as gpx_file_location:
        gps_traj = parse_gpx_file(gpx_file_location)

    gpx_route = "DS7_route"
    with open(f'../DS/{gpx_route}.gpx', 'r') as gpx_file:
        gps_route = parse_gpx_file(gpx_file)

    # Create Simple Grid Map
    cell_sizes = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]
    cell_sizes = [1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,]

    for cell_size in cell_sizes:
        grid_cells = create_simple_gridmap(gps_traj, cell_size)
        visualize_fences(grid_cells, cell_size, filename)