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
    ds1_simp = [[0.25, 0.031963632106781006, 0.00042880639451947075], [0.5, 0.013956561088562011, 0.00019062141745373044], [0.75, 0.010125606060028077, 0.00015522104820347396], [1, 0.008549342155456543, 0.00012818705558734707]]
    ds1_simp_tol = [[0.25, 0.03163492679595947, 0.0003084811306027855], [0.5, 0.013798177242279053, 0.00022217927452205778], [0.75, 0.009921107292175293, 0.00015812065634491292], [1, 0.008261582851409911, 9.208860146273976e-05]]
    ds1_quad = [[1, 0.002520601749420166, 8.076935207754958e-05], [3, 0.016427927017211914, 0.0002305276768323097], [5, 0.08150389909744263, 0.0014599017056169585], [7, 0.29623296976089475, 0.003634495015813387]]
    ds1_quad_tol = [[1, 0.002523820400238037, 6.465747125234162e-05], [3, 0.017146418094635008, 0.00014743134695868347], [5, 0.08292895078659057, 0.0024472797686501038], [7, 0.3020068430900574, 0.005206064777906208]]
    ds2_simp = [[1, 0.05672940015792847, 0.0004312766400148443], [4, 0.011916005611419677, 0.0002167353070890074], [7, 0.007562916278839111, 0.000112298637312814], [10, 0.005262472629547119, 5.89700849633085e-05]]
    ds2_simp_tol = [[1, 0.05685949563980103, 0.00038665989682453003], [4, 0.012093544006347656, 0.00014513250577690838], [7, 0.007925584316253662, 0.00035198534446787076], [10, 0.00543325424194336, 0.00024489124345051264]] 
    ds2_quad = [[1, 0.0018576741218566894, 7.364619974390293e-05], [3, 0.011567220687866211, 0.00032371091445600035], [5, 0.053197598457336424, 0.000566149867919245], [7, 0.1945095944404602, 0.0017135009537460986]]
    ds2_quad_tol = [[1, 0.0018443059921264648, 2.5006480302739547e-05], [3, 0.011022548675537109, 9.903029389901109e-05], [5, 0.05257915496826172, 0.0004198730289422464], [7, 0.2040475583076477, 0.0014711697629699403]]

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