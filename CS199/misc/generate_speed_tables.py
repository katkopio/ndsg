from api import speed_violation, parse_gpx_file
import pdb

def generate_latex(gps_data, caption, label, v_type, s, t):
    violations = speed_violation(gps_data, v_type, s, t)

    lst = []
    for v in violations:
        lst.append([v.get("duration"), v.get("time1").strftime("%a, %d %b %Y"), v.get("time1").strftime("%H:%M:%S GMT"), v.get("time2").strftime("%a, %d %b"), v.get("time2").strftime("%Y %H:%M:%S GMT")])

    print("\\begin{table}[ht]")
    print("\\centering")
    print("\\caption{",caption,"}")
    print("\\begin{tabular}{|c|c|c|}")
    print("\\hline")
    print("\\textbf{Duration} & \\textbf{Start} & \\textbf{End} \\\\\hline")
    for i in lst:
        print(f"{i[0]} & {i[1]} & {i[3]} \\\\")
        print(f"& {i[2]} & {i[4]} \\\\ \hline")
    print("\\end{tabular}")
    print("\\label{Tab:",label,"}")
    print("\\end{table}")

if __name__ == '__main__':
    # filename = f"ds1"
    date = "0426"
    filename = f"DS7-6-{date}"
    with open(f'../../DS/{filename}.gpx', 'r') as gpx_file_location:
        gps_data = parse_gpx_file(gpx_file_location)

    s = 60
    t = 0.5

    v_type = "Explicit"
    # caption = f"Dataset 1 - {v_type}"
    # label = "ds1speedingexplicit"
    caption = f"DS2 {date} - {v_type}"
    label = f"{date}speedingexplicit"
    generate_latex(gps_data, caption, label, v_type, s, t)
    print()
    
    # v_type = "Location"
    # caption = f"Dataset 1 - {v_type}"
    # label = "ds1speedinglocation"
    caption = f"DS2 {date} - {v_type}"
    label = f"{date}speedinglocation"
    generate_latex(gps_data, caption, label, v_type, s, t)