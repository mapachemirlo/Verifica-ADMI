#!/usr/bin/python

import funcionesHard
import sys, os
import re, glob
import time
from getopt import gnu_getopt, GetoptError



def mostrarInfoHard():
    print "[*]Diagnosticando hardware"

    print "\nPROCESADORES: "
    print "Cantidad: " + str(funcionesHard.contarMicroprocesador())
    print "Descripcion: " + str(funcionesHard.obtenerDescripcionMicroprocesador())
    
    print "MEMORIA: "
    print "Cantidad (MB): " + str(funcionesHard.contarMemoria())

    print "\nDISCO: "
    print "Cantidad (GB): " + str(funcionesHard.contarTotalDisco())

    print "\nADAPTADORES DE RED: "
    print "Cantidad: " + str(funcionesHard.contarAdaptadoresRed())

    print "\nADAPTADORES DE VIDEO: "
    print "Cantidad: " + str(funcionesHard.contarAdaptadoresVideo())

    print "\nADAPTADORES DE AUDIO: "
    print "Cantidad: " + str(funcionesHard.contarAdaptadoresAudio())

    print "\nADAPTADORES MULTIMEDIA: "
    print "Cantidad: " + str(funcionesHard.contarAdaptadoresMultimedia())

    print "\nMODEM: "
    print "Cantidad: " +  str(funcionesHard.contarModem())

    print "\nLECTORA: "
    print "Tipo: " + str(funcionesHard.tipoLectora())

    print "\nFLOPPY: "
    print "Cantidad: " + str(funcionesHard.buscarFloppy())

    print "\nSISTEMA OPERATIVO: "
    print "Arandas Linux: " + str(funcionesHard.buscarSisOperativo())

    



