#!/bin/env python
#---------------------------------------------------------------------------
# Anode_GUI module
# Only to be invoked once
# Creates GUI for Anode
#---------------------------------------------------------------------------
import sys
import numpy as np
import time
import threading
import tkinter as tk
from PIL import Image,ImageTk,ImageFile
import Anode_Server as server

ImageFile.LOAD_TRUNCATED_IMAGES = True
#Option calculations
rft = 10 #refresh delay in ms

#Root window instance
rt = tk.Tk()

class KeyHandle(): #Single key handling
    def __init__(self,keycode,send=True,func=None,args=(None),onState=True):
        #True- > Keydown False-> Keyup
        self.keycode = keycode
        self.pressed = False
        self.hasFunction = bool(func)
        self.func = func
        self.funcargs = args
        self.onState= onState
        self.send= send
        self.refresh(keycode,False) #Resets on initialization
    def __repr__(self):
        return f"Key <{self.keycode}>,s:{self.send} f:{self.func}"
    def isPressed(self): #state getter
        return self.pressed
    def refresh(self,key,state):
        #check if not redundant and if the key matches
        if state != self.pressed and key == self.keycode:
            #set pressed
            self.pressed = state
            #send packet
            if self.send:
                server.signal(self.keycode.to_bytes(2,byteorder='big',signed=False),2+int(state))
                #CAfunc: 2-4:keyset(key,0-2)
            if self.hasFunction and state == self.onState:
                self.func(*self.funcargs) #executes added function
            return True
        return False

CATHkeyWin ={49:7,
             87:25,
             65:38,
             83:39,
             68:40,
             103:79,
             104:80,
             105:81,
             100:83,
             101:84,
             102:85,
             97:87,
             98:88}

class KeyHandleGroup(): #Adds proper keydown and keyup support
    keys = []
    def __init__(self,keylist = None):
        if keylist:
            self.keys = keylist
    def addKey(self,key):
        self.keys.append(key)
    def onKeyDown(self,ev): #Wrapper
        self.keyedit(ev,True)
    def onKeyUp(self,ev):   #Wrapper
        self.keyedit(ev,False)
    def keyedit(self,ev,state): #Refreshes the keys until the actual one is found
        sym = ev.keycode #linux keys
        #sym = CATHkeyWin.get(ev.keycode,0) #windows 10 keys
        #print(sym)
        for key in self.keys:
            if key.refresh(sym,state):
                return
#Keyhandlegroup
keygroup=KeyHandleGroup()
#Keymap for Cathode stuff (in keycodes)
CATHkey =[7,25,38,39,40,79,80,81,83,84,85,87,88] #linux config

def endall(): #Ends all operations
    server.signal(b'aaaa',255) #Breaks handle function
    rt.destroy() #Kills tk

class Anode_Win(tk.Frame):
    #initialize shown
    #makes the label the image is shown in
    #initialization
    def __init__(self,master=rt):
        tk.Frame.__init__(self,master)
        self.img = ImageTk.PhotoImage(server.outimage.getimg())
        self.canvas = tk.Canvas(self, width=640, height=480)
        self.canvas.grid(row=0, column=0)
        self.pack()

    def ferr(self,n):
        print(f"function {n} not found")
    #refresh function
    def refr(self):
        #Get shown refreshed
        while not server.outimage.Updated: pass
        self.img=ImageTk.PhotoImage(server.outimage.getimg())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        self.master.after(rft,self.refr) #Schedule new refresh
    #event loop start
    def start(self):
        self.master.after(rft+500,self.refr) #Schedule first refresh
        self.keybinds()
        self.master.mainloop()
    #initialization of binds
    def keybinds(self):
        #Additional anode keybinds go here:
        #Killkey
        keygroup.addKey(KeyHandle(89,send=False,func=endall,args=()))
        #-=---------=-
        for i in CATHkey: #adding cathode keys
            keygroup.addKey(KeyHandle(i))
        print(keygroup.keys)
        #binding keygroup to proper events
        self.bind_all('<KeyPress>', keygroup.onKeyDown)
        self.bind_all('<KeyRelease>' , keygroup.onKeyUp)
        #TODO Learn Tkinter events better, this KeyHandle solution might be unnecessary


if __name__ == "__main__":
    w=Anode_Win() #make Anode_Win instance
    s = threading.Thread(target=server.start)
    s.start() #start Anode_Server
    print('starting GUI')
    w.start() #start Anode_Win
