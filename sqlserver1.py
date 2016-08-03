#! /usr/bin/env python

import pymssql
import sys, os
import re, glob
import time
from getopt import gnu_getopt, GetoptError



# Metodo para conectar a la db
def Conectar(query):

    con = pymssql.connect(host='10.0.0.10', user='sa', password='', database='EProduccionv2')
    cur = con.cursor()

    cur.execute(query)

    result = []
    while 1:
        result = result + cur.fetchall()
        if 0 == cur.nextset():
            break

    con.commit()
    con.close()
    return result
