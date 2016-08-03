#!/usr/bin/python

# Fecha de inicio: 10/2007

import funcionesHard
import diagnosticarHardware
import verificarhardware
import sys, os


print "Modulo de verificacion de hardware"
opc = sys.argv[1:]
#rec = os.system("/usr/local/bin/edpc/flop4.sh")
if ("-diag") in opc:
	funcionesHard.borrarPantalla()
	diagnosticarHardware.mostrarInfoHard()	

else:
        funcionesHard.borrarPantalla()
	verificarhardware.verificarHardware()
