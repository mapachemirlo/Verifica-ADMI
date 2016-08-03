#!/usr/bin/python

# Fecha de inicio: 10/2007

import sys, os
import re, glob
import time
from getopt import gnu_getopt, GetoptError



# Definiciones
pcidev = os.popen("lspci -nn").readlines()
out = sys.stdout

def contarAdaptadoresMultimedia():
    cant = 0
    for line in pcidev:
        if "Multimedia controller" in line:
            cant = cant + 1           
   
    return cant
	    
def contarAdaptadoresVideo():
    cant = 0
    for line in pcidev:
        if "VGA" in line:
            cant = cant + 1           
    
    return cant

def contarAdaptadoresAudio():
    cant = 0
    for line in pcidev:
        if "Audio Device" in line:
            cant = cant + 1
        if "Multimedia audio controller" in line:
            cant = cant + 1           
    
    return cant

def contarAdaptadoresRed():
    cant = 0
    for line in pcidev:
        if "Ethernet" in line:
            cant = cant + 1           
    return cant

def contarModem():
    cant = 0
    for line in pcidev:
        if "Modem" in line:
            cant = cant + 1           
   
    return cant

def contarMicroprocesador():
    cpu = open("/proc/cpuinfo").readlines()
    cant = 0
    for i in cpu:
        if "model name" in i:
            cant = cant + 1
    return cant
    cpu.close()

def obtenerDescripcionMicroprocesador():
    cpu = open("/proc/cpuinfo").readlines()
    for i in cpu:
        if "model name" in i:
            descrip = i.split(":")[1]
    return descrip[:-1]
    cpu.close()


def contarMemoria():
    for i in open("/proc/meminfo").readlines():
        if "MemTotal" in i:
            memt = int(i.split()[-2]) / 1024     
    return int(memt)
    
def tipoLectora():  
    idepath = '/proc/ide/'
    devlist = os.listdir(idepath)
    devlist.sort()
    for dev in devlist:
        if 'hdb' in dev:
            tipo = (open(idepath + dev + "/model").readline()[:-1])         
    return tipo[8:-8]

def contarTotalDisco():
    disc = os.popen("sudo fdisk -l").readlines()
    for i in disc:
        if "Disco" in i:
	    corte = i.split(":")[1]
    return int(corte[:-26])
   

def buscarFloppy():
    cant = 0
    archi = open('/home/claudio/Escritorio/conFede/dato.txt','r')
    for linea in archi:	
        if linea != '0\n':	    
	   
            cant = cant + 1
        else:
            out.write("")
    return cant

def buscarSisOperativo():
    for i in open("/proc/filesystems").readlines():
        if "ext3" in i:
            sistOp = 1
        else:
            sistOp = 0
    return sistOp


def borrarPantalla():
    os.popen('/usr/bin/clear')
    
    
