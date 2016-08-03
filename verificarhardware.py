#!/usr/bin/env python

# Fecha de inicio: 10/2007

import pymssql
import sys, os
import re, glob
import time
import sqlserver1
import funcionesHard
from getopt import gnu_getopt, GetoptError

# Definicion
out = sys.stdout



def verificarHardware():
    
    print "[*]Verificando hardware"
    
    # Ingreso y validacion de numero de serie.
    numSerie = raw_input('[*]Ingrese numero de serie del equipo: ')
    idModelList = sqlserver1.Conectar("SELECT idModel FROM Products WHERE NroSerieProduct = '" + numSerie + "' ")
    cantRegistros = len(idModelList)
    if cantRegistros !=1 :
        if cantRegistros > 1:
            out.write ("\n\tSe produjo un error al encontrarse mas de un numero de serie.\n\n")
            return
        else:
            out.write ("\n\tEl numero de serie "+ numSerie + " no existe.\n\n")
	    return
    idModel = str(idModelList[0][0])

 
    #validar Products.LastState = 0 numSerie
    lastSt = sqlserver1.Conectar("SELECT LastState FROM Products WHERE NroSerieProduct = '" + numSerie + "' ")
    lastState = int(lastSt[0][0])
    if lastState != 0:
        out.write ("Se detiene el proceso porque el producto no esta en el estado correcto.\n\n")
	return
                
    if lastState == 0:
        out.write("Inicia el proceso de verificacion ...\n\n")
           
    #Verificar que el modelo exista en la tabla Models.
    idModelList = sqlserver1.Conectar("SELECT idModel FROM Models WHERE idModel = '" + idModel + "' ")
    cantRegistros = len(idModelList)
    if cantRegistros !=1 :
        out.write ("\n\tSe detiene el proceso porque no se ha encontrado el modelo " + idModel + " en la tabla de modelos.\n\n")
        return


    ####### Hardware ########
    # Variables de trabajo.
    estadoError = 0
 
    ## Procesador ##
    print "PROCESADORES"
    SQL = "SELECT ProcesadorChequea, ProcesadorCantidad, ProcesadorDescripcion FROM Models WHERE idModel = '" + idModel +"' "
    dbListaRed = sqlserver1.Conectar(SQL)
    ChequeaTipoHardware = dbListaRed[0][0]
    TipoHardwareCantidad = dbListaRed[0][1]
    TipoHardwareDescripcion = dbListaRed[0][2]
    if ChequeaTipoHardware != True:
        nChequeaHard = 0
        print "No se verifica"
    else:
        nChequeaHard = 1
        cantidadReal = funcionesHard.contarMicroprocesador()
        print "Cantidad del modelo: " + str(TipoHardwareCantidad)
        print "Cantidad real: " + str(cantidadReal)
        descripcionReal = funcionesHard.obtenerDescripcionMicroprocesador()
        descripcionReal = descripcionReal[1:]
        print "Descripcion del modelo: " + TipoHardwareDescripcion
        print "Descripcion real: " + descripcionReal

        if (cantidadReal != TipoHardwareCantidad) or (TipoHardwareDescripcion != descripcionReal):
           
            estadoError = 1
            print "Estado: ERROR"
        else:
            print "Estado: OK"
        print ""
        SQL = "UPDATE Products SET ProcesadorChequea = " + str(nChequeaHard) + ", ProcesadorCantidad= "+ str(TipoHardwareCantidad) + ", ProcesadorResultadoCantidad = " + str(cantidadReal) + ", ProcesadorDescripcion = '" + TipoHardwareDescripcion + "', ProcesadorResultadoDescripcion = '" + descripcionReal + "' WHERE idModel = '" + idModel + "' AND NroSerieProduct = '" + numSerie + "'"
        sqlserver1.Conectar(SQL)


    ## Disco ##
    print "DISCO DURO"
    SQL = "SELECT DiscoChequea, DiscoDesde, DiscoHasta FROM Models WHERE idModel = '" + idModel +"' "
    dbListaRed = sqlserver1.Conectar(SQL)
    ChequeaTipoHardware = dbListaRed[0][0]
    DiscoDesde = dbListaRed[0][1]
    DiscoHasta = dbListaRed[0][2]
    if ChequeaTipoHardware != True:
        nChequeaHard = 0
        print "No se verifica"
    else:
        nChequeaHard = 1
        cantidadReal = funcionesHard.contarTotalDisco()
        print "Cantidad del modelo: entre " + str(DiscoDesde) + " y " + str(DiscoHasta) + " GB"
        print "Cantidad real: " + str(cantidadReal)
        if (cantidadReal < DiscoDesde) or (cantidadReal > DiscoHasta):
            estadoError = 1
            print "Estado: ERROR"
        else:
            print "Estado: OK"
        print ""
        SQL = "UPDATE Products SET DiscoChequea = " + str(nChequeaHard) + ", DiscoDesde = "+ str(DiscoDesde) + ", DiscoHasta = "+ str(DiscoHasta) + ", DiscoResultado = " + str(cantidadReal) + " WHERE idModel = '" + idModel + "' AND NroSerieProduct = '" + numSerie + "'"
        sqlserver1.Conectar(SQL)


    ## Memoria ##
    print "MEMORIA"
    SQL = "SELECT MemoriaChequea, MemoriaDesde, MemoriaHasta FROM Models WHERE idModel = '" + idModel +"' "
    dbListaRed = sqlserver1.Conectar(SQL)
    ChequeaTipoHardware = dbListaRed[0][0]
    MemoriaDesde = dbListaRed[0][1]
    MemoriaHasta = dbListaRed[0][2]
    if ChequeaTipoHardware != True:
        nChequeaHard = 0
        print "No se verifica"
    else:
        nChequeaHard = 1
        cantidadReal = funcionesHard.contarMemoria()
        print "Cantidad del modelo: entre " + str(MemoriaDesde) + " y " + str(MemoriaHasta) + " MB"
        print "Cantidad real: " + str(cantidadReal)
        if (cantidadReal < MemoriaDesde) or (cantidadReal > MemoriaHasta):
            estadoError = 1
            print "Estado: ERROR"
        else:
            print "Estado: OK"
        print ""
        SQL = "UPDATE Products SET MemoriaChequea = " + str(nChequeaHard) + ", MemoriaDesde = "+ str(DiscoDesde) + ", MemoriaHasta = "+ str(DiscoHasta) + ", MemoriaResultado = " + str(cantidadReal) + " WHERE idModel = '" + idModel + "' AND NroSerieProduct = '" + numSerie + "'"
        sqlserver1.Conectar(SQL)


    ## Red ##
    print "ADAPTADORES DE RED"
    SQL = "SELECT AdaptadorRedChequea, AdaptadorRedCantidad FROM Models WHERE idModel = '" + idModel +"' "
    dbListaRed = sqlserver1.Conectar(SQL)
    ChequeaTipoHardware = dbListaRed[0][0]
    TipoHardwareCantidad = dbListaRed[0][1]
    if ChequeaTipoHardware != True:
        nChequeaHard = 0
        print "No se verifica"
    else:
        nChequeaHard = 1
        cantidadReal = funcionesHard.contarAdaptadoresRed()
        print "Cantidad del modelo: " + str(TipoHardwareCantidad)
        print "Cantidad real: " + str(cantidadReal)
        if cantidadReal != TipoHardwareCantidad:
            estadoError = 1
            print "Estado: ERROR"
        else:
            print "Estado: OK"
        print ""
        SQL = "UPDATE Products SET AdaptadorRedChequea = " + str(nChequeaHard) + ", AdaptadorRedCantidad= "+ str(TipoHardwareCantidad) + ", AdaptadorRedResultado = " + str(cantidadReal) + " WHERE idModel = '" + idModel + "' AND NroSerieProduct = '" + numSerie + "'"
        sqlserver1.Conectar(SQL)


    ## Modem ##
    print "MODEMS"
    SQL = "SELECT ModemChequea, ModemCantidad FROM Models WHERE idModel = '" + idModel +"' "
    dbListaRed = sqlserver1.Conectar(SQL)
    ChequeaTipoHardware = dbListaRed[0][0]
    TipoHardwareCantidad = dbListaRed[0][1]
    if ChequeaTipoHardware != True:
        nChequeaHard = 0
        print "No se verifica"
    else:
        nChequeaHard = 1
        cantidadReal = funcionesHard.contarModem()
        print "Cantidad del modelo: " + str(TipoHardwareCantidad)
        print "Cantidad real: " + str(cantidadReal)
        if cantidadReal != TipoHardwareCantidad:
            estadoError = 1
            print "Estado: ERROR"
        else:
            print "Estado: OK"
        print ""
        SQL = "UPDATE Products SET ModemChequea = " + str(nChequeaHard) + ", ModemCantidad= "+ str(TipoHardwareCantidad) + ", ModemResultado = " + str(cantidadReal) + " WHERE idModel = '" + idModel + "' AND NroSerieProduct = '" + numSerie + "'"
        sqlserver1.Conectar(SQL)


    ## Audio ##
    print "ADAPTADORES DE AUDIO"
    SQL = "SELECT DispAudioChequea, DispAudioCantidad FROM Models WHERE idModel = '" + idModel +"' "
    dbListaRed = sqlserver1.Conectar(SQL)
    ChequeaTipoHardware = dbListaRed[0][0]
    TipoHardwareCantidad = dbListaRed[0][1]
    if ChequeaTipoHardware != True:
        nChequeaHard = 0
        print "No se verifica"
    else:
        nChequeaHard = 1
        cantidadReal = funcionesHard.contarAdaptadoresAudio()
        print "Cantidad del modelo: " + str(TipoHardwareCantidad)
        print "Cantidad real: " + str(cantidadReal)
        if cantidadReal != TipoHardwareCantidad:
            estadoError = 1
            print "Estado: ERROR"
        else:
            print "Estado: OK"
        print ""
        SQL = "UPDATE Products SET DispAudioChequea = " + str(nChequeaHard) + ", DispAudioCantidad= "+ str(TipoHardwareCantidad) + ", DispAudioResultado = " + str(cantidadReal) + " WHERE idModel = '" + idModel + "' AND NroSerieProduct = '" + numSerie + "'"
        sqlserver1.Conectar(SQL)

    ## Video ##
    print "ADAPTADORES DE VIDEO"
    SQL = "SELECT DispVideoChequea, DispVideoCantidad FROM Models WHERE idModel = '" + idModel +"' "
    dbListaRed = sqlserver1.Conectar(SQL)
    ChequeaTipoHardware = dbListaRed[0][0]
    TipoHardwareCantidad = dbListaRed[0][1]
    if ChequeaTipoHardware != True:
        nChequeaHard = 0
        print "No se verifica"
    else:
        nChequeaHard = 1
        cantidadReal = funcionesHard.contarAdaptadoresVideo()
        print "Cantidad del modelo: " + str(TipoHardwareCantidad)
        print "Cantidad real: " + str(cantidadReal)
        if cantidadReal != TipoHardwareCantidad:
            estadoError = 1
            print "Estado: ERROR"
        else:
            print "Estado: OK"
        print ""
        SQL = "UPDATE Products SET DispVideoChequea = " + str(nChequeaHard) + ", DispVideoCantidad= "+ str(TipoHardwareCantidad) + ", DispVideoResultado = " + str(cantidadReal) + " WHERE idModel = '" + idModel + "' AND NroSerieProduct = '" + numSerie + "'"
        sqlserver1.Conectar(SQL)

    ## Floppy ##
    print "FLOPPY"
    SQL = "SELECT FloppyChequea, FloppyCantidad FROM Models WHERE idModel = '" + idModel +"' "
    dbListaRed = sqlserver1.Conectar(SQL)
    ChequeaTipoHardware = dbListaRed[0][0]
    TipoHardwareCantidad = dbListaRed[0][1]
    if ChequeaTipoHardware != True:
        nChequeaHard = 0
        print "No se verifica"
    else:
        nChequeaHard = 1
        cantidadReal = funcionesHard.buscarFloppy()
        print "Cantidad del modelo: " + str(TipoHardwareCantidad)
        print "Cantidad real: " + str(cantidadReal)
        if cantidadReal != TipoHardwareCantidad:
            estadoError = 1
            print "Estado: ERROR"
        else:
            print "Estado: OK"
        print ""
        SQL = "UPDATE Products SET FloppyChequea = " + str(nChequeaHard) + ", FloppyCantidad= "+ str(TipoHardwareCantidad) + ", FloppyResultado = " + str(cantidadReal) + " WHERE idModel = '" + idModel + "' AND NroSerieProduct = '" + numSerie + "'"
        sqlserver1.Conectar(SQL)

    ## Multimedia ##
    print "ADAPTADORES MULTIMEDIA"
    SQL = "SELECT DispMultimediaChequea, DispMultimediaCantidad FROM Models WHERE idModel = '" + idModel +"' "
    dbListaRed = sqlserver1.Conectar(SQL)
    ChequeaTipoHardware = dbListaRed[0][0]
    TipoHardwareCantidad = dbListaRed[0][1]
    if ChequeaTipoHardware != True:
        nChequeaHard = 0
        print "No se verifica"
    else:
        nChequeaHard = 1
        cantidadReal = funcionesHard.contarAdaptadoresMultimedia()
        print "Cantidad del modelo: " + str(TipoHardwareCantidad)
        print "Cantidad real: " + str(cantidadReal)
        if cantidadReal != TipoHardwareCantidad:
            estadoError = 1
            print "Estado: ERROR"
        else:
            print "Estado: OK"
        print ""
        SQL = "UPDATE Products SET DispMultimediaChequea = " + str(nChequeaHard) + ", DispMultimediaCantidad= "+ str(TipoHardwareCantidad) + ", DispMultimediaResultado = " + str(cantidadReal) + " WHERE idModel = '" + idModel + "' AND NroSerieProduct = '" + numSerie + "'"
        sqlserver1.Conectar(SQL)

    ## Sistema Operativo ##
    print "SISTEMA OPERATIVO LINUX"
    SQL = "SELECT SistemaOperativoChequea, SistemaOperativoLinux FROM Models WHERE idModel = '" + idModel +"' "
    dbListaRed = sqlserver1.Conectar(SQL)
    ChequeaTipoHardware = dbListaRed[0][0]
    TipoSistemaOperativo = dbListaRed[0][1]
    if ChequeaTipoHardware != True:
        nChequeaHard = 0
        print "No se verifica"
    else:
        nChequeaHard == 1
        if TipoSistemaOperativo:
            nTipoSistemaOperativo = 1
            print "Sistema Operativo Linux del modelo: Si"
        else:
            nTipoSistemaOperativo = 0
            print "Sistema Operativo Linux del modelo: No"
        if funcionesHard.buscarSisOperativo():
            SOLinuxReal = 1
            print "Sistema Operativo Linux Instalado: Si"
        else:
            SOLinuxReal = 0
            print "Sistema Operativo Linux Instalado: No"
        if nTipoSistemaOperativo != SOLinuxReal:
            estadoError = 1
            print "Estado: ERROR"
        else:
            print "Estado: OK"
        print ""
        SQL = "UPDATE Products SET SistemaOperativoChequea = " + str(nChequeaHard) + ", SistemaOperativoLinux= "+ str(nTipoSistemaOperativo) + ", SistemaOperativoResultado = " + str(SOLinuxReal) + " WHERE idModel = '" + idModel + "' AND NroSerieProduct = '" + numSerie + "'"
        sqlserver1.Conectar(SQL)


   #Confirmacion del usuario
    if estadoError == 0:
        confirmacion = ""
        while confirmacion != 'S' and confirmacion != 'N' and confirmacion != 's' and confirmacion != 'n':
            confirmacion = raw_input("Aspecto exterior y funcionamiento del equipo correcto (S/N)?: ")
            
        if confirmacion == 'S' or confirmacion == 's':
            SQL = "UPDATE Products SET VerificacionManualEstado = 1, VerificacionManualObs = '' WHERE idModel = '" + idModel + "' AND NroSerieProduct = '" + numSerie + "'"
            sqlserver1.Conectar(SQL)
            imprimirEtiquetaOK()
        else:
            observaciones = raw_input("Favor indique los motivos de rechazo: ")
            SQL = "UPDATE Products SET VerificacionManualEstado = 0, VerificacionManualObs = '" + observaciones + "' WHERE idModel = '" + idModel + "' AND NroSerieProduct = '" + numSerie + "'"
            sqlserver1.Conectar(SQL)
            imprimirEtiquetaError()
    else:
        print ""
        print ""
        print "==================================="
        print "RESULTADO: VERIFICACION CON ERRORES"
        print "==================================="
        print ""
        imprimirEtiquetaError()

        

    
    
        
         
def imprimirEtiquetaOK():     
    return


def imprimirEtiquetaError():     
    return


    
