from datetime import datetime
import csv
import pdb
import sys

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
        date_object = datetime.strptime(datum[i["date"]], '%m-%d-%Y').strftime('%Y-%m-%d')
        print(f"<trkpt lat=\"{datum[i['lat']]}\" lon=\"{datum[i['lon']]}\">")
        print(f"\t<time>{date_object}T{datum[i['time']]}Z</time>")
        print(f"\t<speed>{datum[i['speed']]}</speed>")
        print(f"</trkpt>")
    
    print("</trkseg>")
    print("</trk>")
    print("</gpx>")

if __name__ == "__main__":
    # date = "Jan28"
    date = sys.argv[1]

    file_name = f"{date}.csv"
    data = read_csv(file_name)

    index = {
        "date": 0,
        "time": 1,
        "lat": 4,
        "lon": 5,
        "speed":6
    }

    original_stdout = sys.stdout
    with open(f"{date}.gpx", 'w') as f:
        sys.stdout = f 
        convert_to_gpx(data, index)
        sys.stdout = original_stdout