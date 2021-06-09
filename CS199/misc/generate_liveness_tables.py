from api import check_liveness, parse_gpx_file

def generate_latex(gps_data, time_limit, caption, label):
    segments = check_liveness(gps_data, time_limit)
    violations = segments.get("segments")
    lst = []
    for v in violations:
        lst.append([v.get("liveness"), v.get("time1").strftime("%a, %d %b %Y"), v.get("time1").strftime("%H:%M:%S GMT"), v.get("time2").strftime("%a, %d %b %Y"), v.get("time2").strftime("%H:%M:%S GMT")])

    print("\\begin{table}[ht]")
    print("\\centering")
    print("\\caption{",caption,"}",sep='')
    print("\\begin{tabular}{|c|c|c|}")
    print("\\hline")
    print("\\textbf{Duration} & \\textbf{Start} & \\textbf{End} \\\\\hline")
    for i in lst:
        print(f"{i[0]} & {i[1]} & {i[3]} \\\\")
        print(f"& {i[2]} & {i[4]} \\\\ \hline")
    print("\\end{tabular}")
    print("\\label{Tab:",label,"}",sep='')
    print("\\end{table}")
    print()

if __name__ == '__main__':
    dates = ["0420", "0421", "0422", "0424", "0425", "0426"]
    filenames = [f"DS7-1-{dates[0]}", f"DS7-2-{dates[1]}", f"DS7-3-{dates[2]}", f"DS7-4-{dates[3]}", f"DS7-5-{dates[4]}", f"DS7-6-{dates[5]}", "ds1"]

    for i in range(len(filenames)):
        with open(f'../DS/{filenames[i]}.gpx', 'r') as gpx_file_location:
            gps_data = parse_gpx_file(gpx_file_location)

        time_limit = 1200 if i != 6 else 2
        caption =  f"DS 2 {dates[i]} - Liveness Check" if i != 6 else "DS 1 Liveness Check"
        label = f"{dates[i]}liveness" if i != 6 else "ds1liveness"
        generate_latex(gps_data, time_limit, caption, label)
