#! /usr/bin/python

# Fecha de inicio: 10/2007

import sys, os
import re, glob
import time
from getopt import gnu_getopt, GetoptError

# Definiciones
out = sys.stdout

# Tipos de datos para verificaciones

micro = {'Descripcion':'' ,'Cantidad':''}
memoria = {'Total':''}
red = {'Existencia':'','Cantidad':''}
audio = {'Existencia':'', 'Cantidad':''}
video = {'Existencia':'', 'Cantidad':''}
media = {'Existencia':'','Cantidad':''}
modem = {'Existencia':'', 'Cantidad':''}
disco = {'Total':'', 'Cantidad':''}
lectora = {'Existencia':'', 'Tipo':'', 'Descripcion':''}
floppy = {'Existencia':''}
so = {'Descripcion':''}



def porcentaje(t,f):
     s = float(f) / float(t)
     s = str(s)
     if s == "1.0":
         return "100"
     else:
         return s[2:4]
         
def obtenerInformacionHardware():
    # Ejecucion de lspci para obtener informacion de hardware

    try:
	pcidev = os.popen("lspci -nn").readlines()
    except:
	out.write("Error: No se puedo encontrar 'lspci'\n")
	return

    # Codigo para buscar micro modificado
    out.write("Microprocesador:\n")
    try:
        cant = 0
        cpu = open("/proc/cpuinfo").readlines()
        for i in cpu:
            if "model name" in i:
                nomb = i.split(":")[1]
	        out.write("\tNombre: " + nomb)
	        micro['Descripcion'] = nomb
                #out.write("\nAca lo que se guarda en el campo Descripcion del diccionario: " +"\n\t"+ micro['Descripcion'] + "\n")	
                #out.write("Aca muestro todo el diccionario para probar si se agrego Descripcion: \n")
                #print micro
                cant = cant + 1
        if cant != 0:
            out.write("\n\tCantidad de nucleos: " + str(cant) + "\n")
	    micro['Cantidad'] = cant
    except:
        out.write("Problemas al detectar el microprocesador del sistema.\n")
        cpu.close()
    
    # Verificacion de cantidad de memoria
    out.write("Memoria:\n")
    for i in open("/proc/meminfo").readlines():
        if "MemTotal" in i:
            memt = int(i.split()[-2]) / 1024
    out.write("\tTotal RAM:\t%iM" % (memt))
    memoria['Total'] = memt
    
    out.write("\n\n")
	
    # Verificar red del sistema
    cant = 0
    out.write("Adaptadores de red:\n")
    exis = ""
    flag = 0
    for line in pcidev:
        if "Ethernet" in line:
            exis = "si"
            flag = 1
            out.write("\tTipo: %s" % (line[8:]).split("[")[0])
            out.write("\n\tNombre: %s" % ((line.split(":")[2]).split("[")[0]))
           # out.write("\n\tPCIID: %s" % ((line.split(" [")[ (len(line.split(" [")) -1)])).split("] ")[0])
	    red['Existencia'] = exis
	    cant = cant + 1
	    out.write("\n\n")
    if flag == 0:
        out.write("\tNo se detectaron adaptadores de red en el sistema\n")
        exis = "no"
        red['Existencia'] = exis
	red['Cantidad'] = "0"
    if cant != 0:    
	out.write("\tCantidad de adaptadores de red: " + str(cant) + "\n\n")
	red['Cantidad'] = cant

    # Verificar controladores de audio
    out.write("Adaptadores de audio:\n")
    exis = ""
    flag = 0
    cant = 0
    for line in pcidev:
        if "Audio device" in line:
            flag = 1
            exis = "si"
            out.write("\tTipo: %s" % (line[8:]).split("[")[0])
            out.write("\n\tNombre: %s" % ((line.split(":")[2]).split("[")[0]))
           # out.write("\n\tPCIID: %s" % ((line.split(" [")[ (len(line.split(" [")) -1)])).split("] ")[0])
            audio['Existencia'] = exis
	    cant = cant + 1
            
        if "Multimedia audio controller" in line:
	    flag = 1
            exis = "si"
            out.write("\tTipo: %s" % (line[8:]).split("[")[0])
            out.write("\n\tNombre: %s" % ((line.split(":")[2]).split("[")[0]))
           # out.write("\n\tPCIID: %s" % ((line.split(" [")[ (len(line.split(" [")) -1)])).split("] ")[0]) 
            audio['Existencia'] = exis
	    cant = cant + 1
    
    out.write("\n")
    if flag == 0:
        out.write("\tNo se detectaron adaptadores de audio en el sistema\n")
        exis = "no"
        audio['Existencia'] = exis
	audio['Cantidad'] = "0"
    if cant != 0:
	out.write("\n\tCantidad de adaptadores de audio: " + str(cant) + "\n")
        audio['Cantidad'] = cant
    out.write("\n")
    
    # Verificacion de adaptadores de video
    out.write("Adaptadores de video:\n")
    exis = ""
    flag = 0
    cant = 0
    for line in pcidev:
        if "VGA" in line:
            flag = 1
            exis = "si"
            out.write("\tTipo: %s" % (line[8:]).split("[")[0])
            out.write("\n\tNombre: %s" % ((line.split(":")[2]).split("[")[0]))
	   # out.write("\n\tPCIID: %s" % ((line.split(" [")[ (len(line.split(" [")) -1)])).split("] ")[0])
            video['Existencia'] = exis
            cant = cant + 1
    out.write("\n")
    if flag == 0:
        out.write("\tNo se detectaron adaptadores de video en el sistema\n")
        exis = "no"
        video['Existencia'] = exis
	video['Cantidad'] = "0"
    if cant != 0:
	out.write("\n\tCantidad de adaptadores de video: " + str(cant) + "\n")
        video['Cantidad'] = cant

    
    # Verificar controladores multimedia
    out.write("\nAdaptadores multimedia:\n")
    exis = ""
    flag = 0
    cant = 0
    for line in pcidev:
        if "Multimedia controller" in line:
            flag = 1
            exis = "si"
            out.write("\tTipo: %s" % (line[8:]).split("[")[0])
            out.write("\n\tNombre: %s" % ((line.split(":")[2]).split("[")[0]))
           # out.write("\n\tPCIID: %s" % ((line.split(" [")[ (len(line.split(" [")) -1)])).split("] ")[0])
            media['Existencia'] = exis
            cant = cant + 1
    out.write("\n")
    if flag == 0:
        out.write("\tNo se detectaron adaptadores multimedia en el sistema\n\n")
	exis = "no"
	media['Existencia'] = exis
	media['Cantidad'] = "0"
    if cant != 0:
	out.write("\n\tCantidad de adaptadores multimedia: " + str(cant) + "\n")
	media['Cantidad'] = cant
       
    
    # Verificar modems del sistema
    out.write("Modem:\n")
    exis = ""
    flag = 0
    cant = 0
    for line in pcidev:
        if "Modem" in line:
            flag = 1
	    exis = "si"
            out.write("\tTipo: %s" % (line[8:]).split("[")[0])
            out.write("\n\tNombre: %s" % ((line.split(":")[2]).split("[")[0]))
           # out.write("\n\tPCIID: %s" % ((line.split(" [")[ (len(line.split(" [")) -1)])).split("] ")[0])
	    modem['Existencia'] = exis
	    cant = cant + 1
    out.write("\n")
    if flag == 0:
        out.write("\tNo se detectaron modems en el sistema\n")
	exis = "no"
	modem['Existencia'] = exis
	modem['Cantidad'] = "0"
    if cant != 0:
	out.write("\n\tCantidad de modems del sistema: " + str(cant) + "\n")
	modem['Cantidad'] = cant
    
    # Verificar dispositivos IDE ( Lectoras )
    cant = 0
    exis = ""
    idepath = '/proc/ide/'
    devlist = os.listdir(idepath)
    devlist.sort()
    out.write("\nLectoras:\n")
    for dev in devlist:
        if 'hdb' in dev:
	    exis = "si"
            dtype = open(idepath + dev + "/media").readline()[:-1]
            out.write("\tTipo: %s" % (dtype))
	    lectora['Tipo'] = dtype
            modelo = (open(idepath + dev + "/model").readline()[:-1])
            out.write("\n\tModelo: %s" % (open(idepath + dev + "/model").readline()[:-1]))
	    lectora['Descripcion'] = modelo
            out.write("\n\n")
	    lectora['Existencia'] = exis
	    cant = cant + 1
    
    out.write("\nDiscos: ")
    # Verificar dispositivos SATA 
    try:
            for line in open("/proc/scsi/scsi").readlines():
                if "Model" in line:
            	    out.write("\n\tModelo: %s" % (line.split("Model: ")[1]).split(" Rev")[0].split("  ")[0])                
		    cant = cant + 1
	        if "Type" in line:
		    out.write("\n\tTipo: %s" % (line.split("Type: ")[1]).split(" ANSI")[0])
		    out.write("\n")
    except:
        out.write("\tNo se puede obtener informacion de dispositivos SATA en el sistema.\n")
    if cant != 0:
	out.write("\n\tCantidad de dispositivos de almacenamiento: " + str(cant) + "\n")     
    
    disc = os.popen("fdisk -l").readlines()
    for i in disc:
        if "Disco" in i:
	    corte = i.split(":")[1]
	    out.write("\n\tTotal: %s" % corte[:-21] +"\n")
            print "\n"

    # Verificar disketeras
    out.write("\nUnidad de diskettes:\n")
    try:
        archi = open('/tmp/dato.txt','r')
        for linea in archi:	
	    if linea != '0\n':	    
	        out.write("\tSe detectó unidad de diskettes\n\n")
            else:
		out.write("\tNo se detecto unidad de diskettes.")
    except:
        out.write("\tInstalación :######## Error ########\n") 
        out.write("\t\t\tProblema al leer Datos guardados en /tmp")
    out.write("\n")
    
    # Verificacion de BIOS
    out.write("\nFecha del sistema: ")
    out.write(time.strftime("%d/%m/%Y %H:%M"))
    out.write("\n")

   
