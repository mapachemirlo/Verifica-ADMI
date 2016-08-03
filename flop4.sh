#!/bin/bash
# Autor: Claudio Herrera - Daniel Padula
# Fecha de inicio: 10/2007
#

# Buscando floppy
echo ''
echo "Analizando y guardando información ..."
echo ''

#if mount -t vfat /dev/fd0/ /mnt
if [ -b /dev/fd0 ]
then
echo "¡¡¡¡Se encontro lectora, ahora se va a intentar escribir algo en ella si hay disquetera..!!!"

    if [ -r /home/claudio/Desktop/edpc/dato.txt ]
    then
	    sudo rm /home/claudio/Desktop/edpc/dato.txt
	    # Creo el archivo 
	    sudo touch /home/claudio/Desktop/edpc/dato.txt
	    if  dd if=/home/claudio/Desktop/edpc/dato.txt of=/dev/fd0 conv=sync 
	    then 	
		    VAR=1 
	    	    echo " -- Se pudo escribir en floppy Disk --( Esto es a modo de info para mi... )"
		    echo ''
		    echo $VAR > dato.txt
		    echo "Información guardada con exito,se continua el proceso."
	    else
		    VAR=0
	      	    echo  " -- No se pudo escribir en floppy Disk --( Esto es a modo de info para mi... ) "
		    echo ''
	     	    echo $VAR > dato.txt
		    echo "Información guardada con exito,se continua el proceso."
	    fi
    else
	    sudo touch /home/claudio/Desktop/edpc/dato.txt
	    if  dd if=/home/claudio/Desktop/edpc/dato.txt of=/dev/fd0 conv=sync 
	    then 	
		    VAR=1 
	      	    echo " -- Se pudo escribir en floppy Disk --( Esto es a modo de info para mi... )"
		    echo ''
		    echo $VAR > dato.txt
		    echo "Información guardada con exito,se continua el proceso."
	    else
		    VAR=0
	      	    echo  " -- No se pudo escribir en floppy Disk --( Esto es a modo de info para mi... ) "
		    echo ''
		    echo $VAR > dato.txt
		    echo "Información guardada con exito,se continua el proceso."
	    fi
	fi
#umount /mnt/	
else

    echo "¡¡¡NO HAY NINGUNA DISQUETERA NI SIQUIERA SE INTENTO ESCRIBIR UNA MIERDA..!!!"
    
fi	
