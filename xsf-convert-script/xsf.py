# coding=utf-8

import m_xsf
import glob
import os

count=0
todo=glob.glob("*")
for folder in todo:
    if folder=="pseudo-potentials" or folder=="resultados_xsf": continue

    count+=1
    idout=str(count)
    if len(idout)==1: idout="0"+idout
    id=folder[:2]
    elemento=folder[7:]

    if os.path.isdir(folder + "/in_files/axial_deform_x"): simetria=1
    if os.path.isdir(folder + "/in_files/axial_deform_z"): simetria=2
    if os.path.isdir(folder + "/in_files/axial_deform_y"): simetria=3


    m_xsf.xsf(elemento,id,idout,simetria,".","./resultados_xsf")