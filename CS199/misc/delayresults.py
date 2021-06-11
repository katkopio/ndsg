def generate_latex(caption, label, ds):
    size = []
    time = []
    elapsed = []
    for i in ds:
        size.append(i[0])
        time.append(round(i[1],4))
        elapsed.append(f"$\pm$ {round(i[2],4)}")

    print("\\begin{table}[ht]")
    print("\caption{",caption,"}",sep="")
    print("\\resizebox{\columnwidth}{!}{%")
    print("\\begin{tabular}{|c|c|c|c|c|} ")
    print("\hline")
    print("& \\textbf{",size[0]," km} & \\textbf{",size[1]," km} & \\textbf{",size[2]," km} & \\textbf{",size[3]," km}\\\\ \hline",sep="")
    print("\\textbf{{Time}} & {",time[0],"} & {",time[1],"} & {",time[2],"} & {",time[3],"} \\\\ ", sep="")
    print("\\textbf{{Elapsed}} & {",elapsed[0],"} & {",elapsed[1],"} & {",elapsed[2],"} & {",elapsed[3],"} \\\\ \hline", sep="")
    print("\end{tabular}")
    print("\label{",label,"}", sep="")
    print("}")
    print("\end{table}")
    print()
    
if __name__ == '__main__':
    # Output results of runningtests.py
    ds1_simp = [[0.25, 0.07212039947509766, 0.001441138232988424], [0.5, 0.03112149953842163, 0.0002352763389999174], [0.75, 0.022478926181793212, 8.64042654685487e-05], [1, 0.01867218017578125, 0.0001881442755800748]]
    ds1_simp_tol = [[0.25, 0.07068437099456787, 0.00021542506029646768], [0.5, 0.030613555908203124, 0.0009264154720442824], [0.75, 0.02233265161514282, 0.0014561404600233322], [1, 0.018274822235107423, 0.00010714569531994994]]
    ds1_quad = [[1, 0.00502812385559082, 4.739162666237375e-05], [3, 0.03316993951797485, 0.00011526794907004813], [5, 0.1617075777053833, 0.0009175159937056695], [7, 0.5886504411697387, 0.0043849434832039695]]
    ds1_quad_tol = [[1, 0.005048525333404541, 0.00020516873630083477], [3, 0.03317484617233277, 0.00018336773805972082], [5, 0.16176869392395019, 0.0026153160090612165], [7, 0.5936560297012329, 0.0037410780538980155]]
    ds2_simp = [[1, 0.17025168657302855, 0.002965082304896848], [4, 0.03510436534881592, 0.0004198900899457469], [7, 0.022654109001159668, 9.09172166144769e-05], [10, 0.01580765247344971, 0.00010084331361674548]]
    ds2_simp_tol = [[1, 0.16804075002670288, 0.0027025949936061375], [4, 0.03453078746795654, 0.0002612725232771169], [7, 0.02200455904006958, 6.130291576735724e-05], [10, 0.015376245975494385, 0.00017562736120387432]]
    ds2_quad = [[1, 0.005157277584075927, 0.00011561764353979112], [3, 0.03225900650024414, 0.00029857711754513065], [5, 0.15073486328125, 0.0020743495109714094], [7, 0.5524124360084534, 0.004327023475873785]]
    ds2_quad_tol = [[1, 0.005151188373565674, 4.6849654889835074e-05], [3, 0.032357645034790036, 0.0003587427757933523], [5, 0.15088098287582397, 0.00029376370747015006], [7, 0.5804954481124878, 0.004356621365710139]]

    caption = [
        "DS 1 Simple Loop Counting Speed", 
        "DS 1 Simple Loop Counting with Tolerance Speed", 
        "DS 1 Quadtree Loop Counting Speed", 
        "DS 1 Quadtree Loop Counting with Tolerance Speed", 
        "DS 2 Simple Loop Counting Speed", 
        "DS 2 Simple Loop Counting with Tolerance Speed", 
        "DS 2 Quadtree Loop Counting Speed", 
        "DS 2 Quadtree Loop Counting with Tolerance Speed"
    ]

    label = [
        "Tab:ds1speed_simp",
        "Tab:ds1speed_simptol",
        "Tab:ds1speed_quad",
        "Tab:ds1speed_quadtol",
        "Tab:ds2speed_simp",
        "Tab:ds2speed_simptol",
        "Tab:ds2speed_quad",
        "Tab:ds2speed_quadtol"
    ]

    lists = [ds1_simp, ds1_simp_tol, ds1_quad, ds1_quad_tol, ds2_simp, ds2_simp_tol, ds2_quad, ds2_quad_tol]

    for i in range(len(caption)):
        generate_latex(caption[i], label[i], lists[i])