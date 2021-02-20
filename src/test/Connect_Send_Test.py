#!/bin/env python
#
# A small test for Connect library
# Made to tweak settings and test for connection 
#

import ANCA_Connect as Con
import socket

SOCK = socket.socket()
func_pass = 0 

SOCK.connect(Con.AADDR)
while True:
    Con.SND(SOCK,input("Input a message").encode('utf-8'),func_pass)
    pac =Con.REC(SOCK)
    print(f"Recieved:\n{pac.decode('utf-8')}")
