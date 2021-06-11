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
    ds2_simp = [[1, 0.12501509189605714, 0.00042346652132406167], [4, 0.02588782548904419, 0.000105251086746948], [7, 0.01652063608169556, 0.0004342390133911021], [10, 0.0117846941947937, 7.313673978051625e-05]]
    ds2_simp_tol = [[1, 0.1258453369140625, 0.002192786240349285], [4, 0.025717663764953613, 0.00011981085790692469], [7, 0.016463029384613036, 4.149986279400773e-05], [10, 0.01148228406906128, 0.00020854159584969022]]
    ds2_quad = [[1, 0.0036852359771728516, 4.516658684709558e-05], [3, 0.022181155681610106, 7.030099152881894e-05], [5, 0.10431164741516114, 0.002551057012233001], [7, 0.3897141456604004, 0.0027489450979389907]]
    ds2_quad_tol = [[1, 0.003727307319641113, 2.225065790055273e-05], [3, 0.02232384920120239, 0.00011158769741267466], [5, 0.10545672416687012, 0.00017852505558680316], [7, 0.4051415109634399, 0.003924610277547878]]

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