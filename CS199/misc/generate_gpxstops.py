def generate_gpx_file(stops):
    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    print("<gpx xmlns=\"http://www.topografix.com/GPX/1/1\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd\" version=\"1.1\" creator=\"gpx.py -- https://github.com/tkrajina/gpxpy\">")

    for stop in stops:
        print(f"<wpt lat=\"{stop[0]}\" lon=\"{stop[1]}\">")
        print("</wpt>")
        print(f"<wpt lat=\"{stop[2]}\" lon=\"{stop[3]}\">")
        print("</wpt>")
    print("</gpx>")

def generate_stop_latex(stops):
    print("\\topcaption{Dataset 2 Stops}")
    print("\\centering")
    print("\\tablefirsthead{\hline \multicolumn{1}{|c|}{\\textbf{Top Left Coordinate}} & \multicolumn{1}{|c|}{\\textbf{Bottom Right Coordinate}} \\\\ \hline}")
    print("\\tablehead{\multicolumn{2}{c} {{\\bfseries  Continued from previous column}} \\\\ \hline \multicolumn{1}{|c|}{\\textbf{Top Left Coordinate}} & \multicolumn{1}{|c|}{\\textbf{Bottom Right Coordinate}} \\\\ \hline}")
    print("\\tabletail{\hline \multicolumn{2}{|r|}{{Continued on next page}} \\\\ \hline}")
    print("\\tablelasttail{\\\\ \hline }")
    print("\\begin{xtabular}{|c|c|}")
    for stop in stops:
        print(f"{round(stop[0],5)}, {round(stop[1],5)} & {round(stop[2],5)}, {round(stop[3],5)} \\\\ \hline")
    print("\\end{xtabular}")
    print("\label{Tab:ds2stops}")

if __name__ == '__main__':
    ds1stops = [[14.65493,121.0584,14.65469,121.05854],[14.65295,121.06244,14.65283,121.06257],[14.65242,121.0686,14.65228,121.06868],[14.64734,121.06877,14.64717,121.06896]]
    ds2stops = [[14.513275870496644,120.98939957311633,14.508926778279776,120.99407143966094],[14.539207227926902,120.98977745396049,14.534694794656243,120.99434626437592],[14.539741525871644,120.99777964043429,14.535203133158655,121.00241449772616],[14.551433092443729,121.02656109759592,14.546926094659344,121.03008015591014],[14.570669866006527,121.04367915508293,14.56630423548145,121.0483283486605],[14.589016713864568,121.05411464043465,14.584718146716531,121.05876022656285],[14.610785707237877,121.0537886770124,14.606674442899923,121.05845572081326],[14.61595968222573,121.05139196927097,14.611848514671594,121.0560482842355],[14.630459228241007,121.04471516927117,14.626327569795327,121.04937148423572],[14.643531658062017,121.03691366927139,14.63974280301566,121.04158071307226],[14.653366694064948,121.03051896927136,14.649526108739387,121.03517528423589],[14.659973665079784,121.0171412692482,14.655468891304901,121.02179758421273],[14.659733608199652,121.00283306927132,14.655228829488141,121.00748938423587],[14.659598189259533,120.99494776927135,14.655093407763232,120.9996040842359],[14.659437711214382,120.98381856927128,14.654932926404847,120.98847488423584]]
    
    # generate_gpx_file(stops)
    generate_stop_latex(ds2stops)