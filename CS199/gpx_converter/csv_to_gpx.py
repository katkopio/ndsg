from datetime import datetime
import csv, sys, pdb

def read_csv(file_name):
    data = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                data.append(row)
            line_count += 1
    return data

def convert_to_gpx(data, i):
    print("<?xml version=\"1.0\" encoding=\"utf-8\"?>")
    print("<gpx version=\"1.0\">")
    print("<trk>")
    print("<trkseg>")

    for datum in data:
        date_time_obj = datetime.strptime(datum[i["datetime"]], '%m/%d/%y %H:%M')
        print(f"<trkpt lat=\"{datum[i['lat']]}\" lon=\"{datum[i['lon']]}\">")
        print(f"\t<time>{date_time_obj.isoformat()}</time>")
        print(f"\t<speed>{datum[i['speed']]}</speed>")
        print(f"</trkpt>")
    
    print("</trkseg>")
    print("</trk>")
    print("</gpx>")

if __name__ == "__main__":
    csv_file = "DS7-6-0426"
    file_name = f"CSV/{csv_file}.csv"
    data = read_csv(file_name)
    index = {
        "datetime": 1,
        "lat": 2,
        "lon": 3,
        "speed":4
    }

    original_stdout = sys.stdout
    with open(f"GPX/{csv_file}.gpx", 'w') as f:
        sys.stdout = f 
        convert_to_gpx(data, index)
        sys.stdout = original_stdout