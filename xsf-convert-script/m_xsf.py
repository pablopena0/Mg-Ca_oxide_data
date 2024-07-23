def xsf_out(infile,outfile):
    qe=open(infile,"r")
    xsf=open(outfile,"w")

    to_search_energy="!"
    n_atoms=""

    #Leemos el archivo linea por linea
    line = qe.readline()
    while line:
        line = qe.readline()
        search = line.split()
        
        #Buscamos número de átomos
        if ("atoms/cell" in search):
            n_atoms = int(search[4])

        #Leemos el alat
        if ("celldm(1)=" in search and type(n_atoms)==int):
            alat=float(search[1]) * 0.5291772
        
        #Buscamos la base
        if ("crystal" in search and type(n_atoms)==int):
            base_x=[]
            base_y=[]
            base_z=[]
            for i in range(3):
                line = qe.readline()
                search = line.split()
                for s in range(3,6): 
                    if abs(float(search[s]))<=0.0000001: search[s]="0.0"
                base_x.append(float(search[3]) * alat)   #Multiplicamos por alat
                base_y.append(float(search[4]) * alat)
                base_z.append(float(search[5]) * alat)


        #Buscamos posciciones
        if ("positions" in search and type(n_atoms)==int):
            element=[]
            possition_x=[]
            possition_y=[]
            possition_z=[]
            for i in range(n_atoms):
                line = qe.readline()
                search = line.split()
                element.append(search[1])
                for s in range(6,9): 
                    if abs(float(search[s]))<=0.000001: search[s]="0.0"
                possition_x.append(float(search[6]) * alat)
                possition_y.append(float(search[7]) * alat)
                possition_z.append(float(search[8]) * alat)

        #Buscamos la energía
        if ("!" in search and type(n_atoms)==int):
            energy=float(search[4]) * 13.6057039763
        
        #Buscamos las fuerzas
        if ("Forces" in search and type(n_atoms)==int):
            qe.readline()
            force_x=[]
            force_y=[]
            force_z=[]
            for i in range(n_atoms):
                line = qe.readline()
                search = line.split()
                force_x.append(float(search[6]) * 0.5 / 0.5291772)      #Pasamos de ry/au a hartree/Amstrong
                force_y.append(float(search[7]) * 0.5 / 0.5291772)
                force_z.append(float(search[8]) * 0.5 / 0.5291772)

    qe.close()

    xsf.write("# total energy = " + str(energy) + " eV\n\n")
    xsf.write("CRYSTAL\n" + "PRIMVEC\n")

    for i in range(3):
        xsf.write("\t\t"+ "{0:.8f}".format(base_x[i]) + "\t\t" + "{0:.8f}".format(base_y[i]) + "\t\t" + "{0:.8f}".format(base_z[i]) + "\n")

    xsf.write("PRIMECORD\n" + "   " + str(n_atoms) + " 1\n")

    for i in range(n_atoms):
        xsf.write(element[i] + "\t\t" + "{0:.8f}".format(possition_x[i]) + "\t\t" + "{0:.8f}".format(possition_y[i]) + "\t\t" + "{0:.8f}".format(possition_z[i]))
        
        if force_x[i]<0.0000000001: xsf.write("\t\t" + "{0:.8f}".format(force_x[i]))
        else: xsf.write("\t\t " + "{0:.8f}".format(force_x[i]))
        if force_y[i]<0.0000000001: xsf.write("\t\t" + "{0:.8f}".format(force_y[i]))
        else: xsf.write("\t\t " + "{0:.8f}".format(force_y[i]))
        if force_z[i]<0.0000000001: xsf.write("\t\t" + "{0:.8f}".format(force_z[i]) + "\n")
        else: xsf.write("\t\t " + "{0:.8f}".format(force_z[i]) + "\n")
        #xsf.write("{0:.8f}".format(force_x[i]) + "\t\t" + "{0:.8f}".format(force_y[i]) + "\t\t" + "{0:.8f}".format(force_z[i]) + "\n")

    xsf.close()


def xsf(elemento,id,simetria,input,output):
    #input: solo el nombre del directorio, sin barras ni nada adicional.
    #output: nombre del directorio del output
    
    import os
    import glob

    out_folder=output+"/"+id+"_"+elemento+"_xsf"+"/"

    #Estructura original
    if not os.path.isdir(out_folder): os.mkdir(out_folder)
    inpath=glob.glob(f"{input}/{id}_{elemento}/in_files/{elemento}.*/{elemento}.out")[0]
    xsf_out(inpath,out_folder+elemento+".xsf")

    #Estructuras deformaciones axiales
    for k in range(4-simetria):
        if k==1: k=2    #Ya que normalmente el eje diferente es el z
        elif k==2: k=1

        out_name={0:"x" , 1:"y" , 2:"z"}
        out_subfolder=out_folder+"axial_deform_"+out_name[k]+"/"
        if not os.path.isdir(out_subfolder): os.mkdir(out_subfolder) #Directorio de las deformaciones axiales

        for n in range(-100,110,25):
            if(n==0): continue
            n=n/10.0
            if n==round(n):
                nombre_deform=str(int(n))
            else:
                if n==-7.5: nombre_deform="-7,5"
                elif n==-2.5: nombre_deform="-2,5"
                elif n==2.5: nombre_deform="2,5"
                elif n==7.5: nombre_deform="7,5"
            inpath=glob.glob(f"{input}/{id}_{elemento}/in_files/axial_deform_{out_name[k]}/{elemento}_deform_{nombre_deform}.*/{elemento}_deform_{nombre_deform}.out")[0]
            xsf_out(inpath,out_subfolder+f"{elemento}_deform_{nombre_deform}.xsf") #Crea los archivos xsf



    #Estructuras deformaciones angulares
    for k in range(4-simetria):
        if k==0: i,j=0,1
        elif k==1: i,j=0,2
        elif k==2: i,j=1,2

        out_name={0:"x" , 1:"y" , 2:"z"}
        out_subfolder=out_folder+"angular_deform_"+out_name[i]+out_name[j]+"/"
        if not os.path.isdir(out_subfolder): os.mkdir(out_subfolder) #Directorio de las deformaciones angulares

        for n in range(-16,17,4):
            if(n==0): continue
            inpath=glob.glob(f"{input}/{id}_{elemento}/in_files/angular_deform_{out_name[i]}{out_name[j]}/{elemento}_deform_{str(n)}.*/{elemento}_deform_{str(n)}.out")[0]
            xsf_out(inpath,out_subfolder+f"{elemento}_deform_{str(n)}.xsf") #Crea los archivos xsf

    #Estructuras deformaciones hidrostáticas
    out_subfolder=out_folder+"hydrostatic_deform/"
    if not os.path.isdir(out_subfolder): os.mkdir(out_subfolder) #Directorio de las deformaciones angulares

    for n in range(-100,110,25):
        if(n==0): continue
        n=n/10.0
        if n==round(n):
            nombre_deform=str(int(n))
        else:
            if n==-7.5: nombre_deform="-7,5"
            elif n==-2.5: nombre_deform="-2,5"
            elif n==2.5: nombre_deform="2,5"
            elif n==7.5: nombre_deform="7,5"
        inpath=glob.glob(f"{input}/{id}_{elemento}/in_files/hydrostatic_deform/{elemento}_deform_hydro_{nombre_deform}.*/{elemento}_deform_hydro_{nombre_deform}.out")[0]
        xsf_out(inpath,out_subfolder+f"{elemento}_deform_hydro_{nombre_deform}.xsf") #Crea los archivos xsf