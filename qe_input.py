# coding=utf-8
#archivos .in para QE a partir del exportado de Vesta con deformaciones axiales entre -10% y +10%, angulares entre +15% y -15%, hidrostáticas entre 10GPa y -10 GPa

import numpy as np
import os

#Parámetros
simetria=2      #1 si no tiene, 2 si tiene 2 ejes iguales, 3 si tiene los 3 ejes iguales
elemento="MgO"
main_folder="./"

#Calculamos la estructura original a partir del exportado de vesta
f_vesta=open(main_folder+elemento+".vasp","r")
f_poss=open(main_folder+"posiciones.txt","w")
f_base=open(main_folder+"base.txt","w")

f_vesta.readline()
f_vesta.readline()
base=[[],[],[]]
for i in range(3):
    vector=f_vesta.readline()
    f_base.write(vector)
    base[i]=[float(x) for x in vector.split()]
    
elements=f_vesta.readline().split()
element_dic={"Mg":"24.305","O":"15.999","H":"1.0078","Si":"28.0855","Ca":"40.078"}
quantity=[int(x) for x in f_vesta.readline().split()]
total=0
for i in quantity: total+=i
dic={elements[x]:quantity[x] for x in range(len(elements))}

f_vesta.readline()
for elem in elements:
    for i in range(dic[elem]):
        f_poss.write(elem+"\t ")
        f_poss.write(f_vesta.readline())
f_vesta.close()
f_poss.close()
f_base.close()

k1=int(round((2*np.pi/np.sqrt(base[0][0]**2+base[0][1]**2+base[0][2]**2))/0.3))
k2=int(round((2*np.pi/np.sqrt(base[1][0]**2+base[1][1]**2+base[1][2]**2))/0.3))
k3=int(round((2*np.pi/np.sqrt(base[2][0]**2+base[2][1]**2+base[2][2]**2))/0.3))


#Estructura cristalina original
for n in range(1):
    in_folder=main_folder+"in_files/"
    if not os.path.isdir(in_folder): os.mkdir(in_folder)
    f_p1=open(main_folder+"script_vesta-qe/plantillaQE_1.txt","r")
    f_p2=open(main_folder+"script_vesta-qe/plantillaQE_2.txt","r")
    f_c1=open(main_folder+"script_vesta-qe/colas_1.txt","r")
    f_c2=open(main_folder+"script_vesta-qe/colas_2.txt","r")
    f_poss=open(main_folder+"posiciones.txt","r")
    f_base=open(main_folder+"base.txt","r")
    f_out=open(in_folder+elemento+".in","w")
    f_cout=open(in_folder+elemento+".slurm","w")

    #Primera plantilla
    for line in f_p1:
        f_out.write(line)
    f_out.write("nat = "+str(total)+", ntyp = "+str(len(elements)))
    
    #Segunda plantilla
    for line in f_p2:
        f_out.write(line)
    
    for p in elements:
        f_out.write(p+" "+element_dic[p]+" "+p+".upf\n")
    f_out.write("\nATOMIC_POSITIONS {angstrom}\n")

    #Posiciones
    for line in f_poss:
        poss=line.split()
        vector=[float(poss[x]) for x in range(1,4)]
        
        f_out.write(poss[0]+"    ")
        for v in vector:    
            f_out.write("{0:.6f}".format(v)+" ")
        f_out.write("\n")
    f_out.write("\n")

    #k points
    f_out.write("K_POINTS {automatic}\n")
    f_out.write(" "+str(k1)+" "+str(k2)+" "+str(k3)+" 0 0 0 \n")
    f_out.write("\nCELL_PARAMETERS {angstrom}\n")

    #Base
    for i in range(3):
        for j in range(3):
            f_out.write(" "+"{0:.6f}".format(base[i][j]))
        f_out.write("\n")


    #Script colas
    for line in f_c1:
        f_cout.write(line)    

    f_cout.write("#SBATCH --workdir=.\n\n")
    f_cout.write("input=\""+elemento+"\"")
    f_cout.write("\n"+"output=\"output\"\nfiles=\"")
    f_cout.write(elemento+".in")
    for e in elements: f_cout.write(" ../../pseudo-potentials/"+e+".upf") 
    f_cout.write("\"\ncommand=\"pw.x -ndiag 1 < ")
    f_cout.write(elemento+".in > "+elemento+".out\" \n")

    for line in f_c2:
        f_cout.write(line)
    

    f_p1.close()
    f_p2.close()
    f_c1.close()
    f_c2.close()
    f_poss.close()
    f_base.close()
    f_out.close()
    f_cout.close()

    os.chdir(in_folder)
    os.system("dos2unix "+elemento+".slurm")
    os.system("sbatch "+elemento+".slurm")
    os.chdir("..")




#Deformaciones axiales
for k in range(4-simetria):
    deform=[[1,0,0]
        ,[0,1,0]
        ,[0,0,1]]
    if k==1: k=2    #Ya que normalmente el eje diferente es el z
    elif k==2: k=1

    out_name={0:"x" , 1:"y" , 2:"z"}
    folder=main_folder+"in_files/axial_deform_"+out_name[k]+"/"
    if not os.path.isdir(folder): os.mkdir(folder) #Directorio de las deformaciones axiales

    for n in range(-100,110,25):
        if(n==0): continue
        n=n/10.0

        epsilon=n/100.0
        deform[k][k]=1.0+epsilon
        base_deform=np.matmul(base,deform)

        f_p1=open(main_folder+"script_vesta-qe/plantillaQE_1.txt","r")
        f_p2=open(main_folder+"script_vesta-qe/plantillaQE_2.txt","r")
        f_c1=open(main_folder+"script_vesta-qe/colas_1.txt","r")
        f_c2=open(main_folder+"script_vesta-qe/colas_2.txt","r")
        f_poss=open(main_folder+"posiciones.txt","r")
        f_base=open(main_folder+"base.txt","r")
        if n==round(n):
            nombre_deform=str(int(n))
        else:
            if n==-7.5: nombre_deform="-7,5"
            elif n==-2.5: nombre_deform="-2,5"
            elif n==2.5: nombre_deform="2,5"
            elif n==7.5: nombre_deform="7,5"
        f_out=open(folder+elemento+"_deform_"+nombre_deform+".in","w")
        f_cout=open(folder+elemento+"_deform_"+nombre_deform+".slurm","w")

        #Primera plantilla
        for line in f_p1:
            f_out.write(line)
        f_out.write("nat = "+str(total)+", ntyp = "+str(len(elements)))
        #Segunda plantilla
        for line in f_p2:
            f_out.write(line)
        
        for p in elements:
            f_out.write(p+" "+element_dic[p]+" "+p+".upf\n")
        f_out.write("\nATOMIC_POSITIONS {angstrom}\n")

        #Calculo de deformaciones
        for line in f_poss:
            poss=line.split()
            vector=[float(poss[x]) for x in range(1,4)]
            vector=np.matmul(vector,deform)
            
            f_out.write(poss[0]+"    ")
            for v in vector:    
                f_out.write("{0:.6f}".format(v)+" ")
            f_out.write("\n")
        f_out.write("\n")

        #k points
        f_out.write("K_POINTS {automatic}\n")
        f_out.write(" "+str(k1)+" "+str(k2)+" "+str(k3)+" 0 0 0 \n")
        f_out.write("\nCELL_PARAMETERS {angstrom}\n")

        #Nueva base
        for i in range(3):
            for j in range(3):
                f_out.write(" "+"{0:.6f}".format(base_deform[i][j]))
            f_out.write("\n")
        

        #Script colas
        for line in f_c1:
            f_cout.write(line)    

        f_cout.write("#SBATCH --workdir=. \n\n")
        f_cout.write("input=\""+elemento+"_deform_"+nombre_deform+"\"")
        f_cout.write("\n"+"output=\"output\"\nfiles=\"")
        f_cout.write(elemento+"_deform_"+nombre_deform+".in")
        for e in elements: f_cout.write(" ../../../pseudo-potentials/"+e+".upf") 
        f_cout.write("\"\ncommand=\"pw.x -ndiag 1 < ")
        f_cout.write(elemento+"_deform_"+nombre_deform+".in > "+elemento+"_deform_"+nombre_deform+".out\"\n")

        for line in f_c2:
            f_cout.write(line)


        f_p1.close()
        f_p2.close()
        f_c1.close()
        f_c2.close()
        f_poss.close()
        f_base.close()
        f_out.close()
        f_cout.close()

        os.chdir(folder)
        os.system("dos2unix "+elemento+"_deform_"+nombre_deform+".slurm")
        os.system("sbatch "+elemento+"_deform_"+nombre_deform+".slurm")
        os.chdir("../..")




#Deformaciones angulares (deformación de cizalla)
for k in range(4-simetria):
    if k==0: i,j=0,1
    elif k==1: i,j=0,2
    elif k==2: i,j=1,2

    deform=[[1,0,0]
        ,[0,1,0]
        ,[0,0,1]]
    
    out_name={0:"x" , 1:"y" , 2:"z"}
    folder=main_folder+"in_files/angular_deform_"+out_name[i]+out_name[j]+"/"
    if not os.path.isdir(folder): os.mkdir(folder) #Directorio de las deformaciones angulares

    for n in range(-16,17,4):
        if(n==0): continue
        
        epsilon=n/100.0
        deform[i][j]=epsilon
        deform[j][i]=epsilon
        base_deform=np.matmul(base,deform)

        f_p1=open(main_folder+"script_vesta-qe/plantillaQE_1.txt","r")
        f_p2=open(main_folder+"script_vesta-qe/plantillaQE_2.txt","r")
        f_c1=open(main_folder+"script_vesta-qe/colas_1.txt","r")
        f_c2=open(main_folder+"script_vesta-qe/colas_2.txt","r")
        f_poss=open(main_folder+"posiciones.txt","r")
        f_base=open(main_folder+"base.txt","r")
        f_out=open(folder+elemento+"_deform_"+str(n)+".in","w")
        f_cout=open(folder+elemento+"_deform_"+str(n)+".slurm","w")

        #Primera plantilla
        for line in f_p1:
            f_out.write(line)
        f_out.write("nat = "+str(total)+", ntyp = "+str(len(elements)))
        #Segunda plantilla
        for line in f_p2:
            f_out.write(line)

        for p in elements:
            f_out.write(p+" "+element_dic[p]+" "+p+".upf\n")
        f_out.write("\nATOMIC_POSITIONS {angstrom}\n")

        #Calculo de deformaciones
        for line in f_poss:
            poss=line.split()
            vector=[float(poss[x]) for x in range(1,4)]
            vector=np.matmul(vector,deform)
            
            f_out.write(poss[0]+"    ")
            for v in vector:    
                f_out.write("{0:.6f}".format(v)+" ")
            f_out.write("\n")
        f_out.write("\n")

        #k points
        f_out.write("K_POINTS {automatic}\n")
        f_out.write(" "+str(k1)+" "+str(k2)+" "+str(k3)+" 0 0 0 \n")
        f_out.write("\nCELL_PARAMETERS {angstrom}\n")

        #Nueva base
        for h in range(3):
            for l in range(3):
                f_out.write(" "+"{0:.6f}".format(base_deform[h][l]))
            f_out.write("\n")


        #Script colas
        for line in f_c1:
            f_cout.write(line)    

        f_cout.write("#SBATCH --workdir=.\n\n")
        f_cout.write("input=\""+elemento+"_deform_"+str(n)+"\"")
        f_cout.write("\n"+"output=\"output\"\nfiles=\"")
        f_cout.write(elemento+"_deform_"+str(n)+".in")
        for e in elements: f_cout.write(" ../../../pseudo-potentials/"+e+".upf") 
        f_cout.write("\"\ncommand=\"pw.x -ndiag 1 < ")
        f_cout.write(elemento+"_deform_"+str(n)+".in > "+elemento+"_deform_"+str(n)+".out\"\n")

        for line in f_c2:
            f_cout.write(line)


        f_p1.close()
        f_p2.close()
        f_c1.close()
        f_c2.close()
        f_poss.close()
        f_base.close()
        f_out.close()
        f_cout.close()

        os.chdir(folder)
        os.system("dos2unix "+elemento+"_deform_"+str(n)+".slurm")
        os.system("sbatch "+elemento+"_deform_"+str(n)+".slurm")
        os.chdir("../..")




#Deformaciones hidrostáticas. Este caso es un poco diferente ya que utilizaremos celdas variables en QE.
folder=main_folder+"in_files/hydrostatic_deform/"
if not os.path.isdir(folder): os.mkdir(folder) #Directorio de las deformaciones angulares

for n in range(-100,110,25):
    if(n==0): continue
    n=n/10.0

    epsilon=n*10.0

    f_p1=open(main_folder+"script_vesta-qe/plantillaQE_1_hydro.txt","r")
    f_p2=open(main_folder+"script_vesta-qe/plantillaQE_2_hydro.txt","r")
    f_p3=open(main_folder+"script_vesta-qe/plantillaQE_3_hydro.txt","r")
    f_c1=open(main_folder+"script_vesta-qe/colas_1_hydro.txt","r")
    f_c2=open(main_folder+"script_vesta-qe/colas_2.txt","r")
    f_poss=open(main_folder+"posiciones.txt","r")
    f_base=open(main_folder+"base.txt","r")
    if n==round(n):
        nombre_deform=str(int(n))
    else:
        if n==-7.5: nombre_deform="-7,5"
        elif n==-2.5: nombre_deform="-2,5"
        elif n==2.5: nombre_deform="2,5"
        elif n==7.5: nombre_deform="7,5"
    f_out=open(folder+elemento+"_deform_hydro_"+nombre_deform+".in","w")
    f_cout=open(folder+elemento+"_deform_hydro_"+nombre_deform+".slurm","w")

    #Primera plantilla
    for line in f_p1:
        f_out.write(line)
    f_out.write("nat = "+str(total)+", ntyp = "+str(len(elements)))
    #Segunda plantilla
    for line in f_p2:
        f_out.write(line)
    
    #Presión
    f_out.write(str(epsilon))

    #Tercera plantilla
    for line in f_p3:
        f_out.write(line)
    
    for p in elements:
        f_out.write(p+" "+element_dic[p]+" "+p+".upf\n")
    f_out.write("\nATOMIC_POSITIONS {angstrom}\n")

    #Posiciones
    for line in f_poss:
        poss=line.split()
        vector=[float(poss[x]) for x in range(1,4)]
        
        f_out.write(poss[0]+"    ")
        for v in vector:    
            f_out.write("{0:.6f}".format(v)+" ")
        f_out.write("\n")
    f_out.write("\n")

    #k points
    f_out.write("K_POINTS {automatic}\n")
    f_out.write(" "+str(k1)+" "+str(k2)+" "+str(k3)+" 0 0 0 \n")
    f_out.write("\nCELL_PARAMETERS {angstrom}\n")

    #Nueva base
    for i in range(3):
        for j in range(3):
            f_out.write(" "+"{0:.6f}".format(base[i][j]))
        f_out.write("\n")
    
    #Script colas
    for line in f_c1:
        f_cout.write(line)    

    f_cout.write("#SBATCH --workdir=.\n\n")
    f_cout.write("input=\""+elemento+"_deform_hydro_"+nombre_deform+"\"")
    f_cout.write("\n"+"output=\"output\"\nfiles=\"")
    f_cout.write(elemento+"_deform_hydro_"+nombre_deform+".in")
    for e in elements: f_cout.write(" ../../../pseudo-potentials/"+e+".upf") 
    f_cout.write("\"\ncommand=\"pw.x -ndiag 1 < ")
    f_cout.write(elemento+"_deform_hydro_"+nombre_deform+".in > "+elemento+"_deform_hydro_"+nombre_deform+".out\"\n")

    for line in f_c2:
        f_cout.write(line)


    f_p1.close()
    f_p2.close()
    f_p3.close()
    f_c1.close()
    f_c2.close()
    f_poss.close()
    f_base.close()
    f_out.close()
    f_cout.close()

    os.chdir(folder)
    os.system("dos2unix "+elemento+"_deform_hydro_"+nombre_deform+".slurm")
    os.system("sbatch "+elemento+"_deform_hydro_"+nombre_deform+".slurm")
    os.chdir("../..")
