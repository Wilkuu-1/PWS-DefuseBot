#!/bin/env python

#
# Small test for tweaking Connect library
# This one sets up a server

import ANCA_Connect as CON
import socket

SOCK = socket.socket()
SOCK.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
SOCK.bind(CON.AADDR)

funcpass = 0
def handle(conn,addr):
    while True:
        pac = CON.REC(conn)
        print(f"Message:\n{pac.decode('utf-8')}")
        CON.SND(conn,input("Reply:\n").encode('utf-8'),funcpass)

SOCK.listen()
while True:
    conn,addr = SOCK.accept()
    handle(conn,addr)
