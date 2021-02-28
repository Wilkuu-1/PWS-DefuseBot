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
from PIL import Image,ImageTk
import Anode_Server as server

#Options
frps = 30 #frame refreshes per second

#Option calculations
rft = int(1000/30) #calculation for frsp

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
        #sym = ev.keycode
        sym = CATHkeyWin.get(ev.keycode,0)
        #print(sym)
        for key in self.keys:
            if key.refresh(sym,state):
                return
#Keyhandlegroup
keygroup=KeyHandleGroup()
#Keymap for Cathode stuff (in keycodes)
CATHkey =[7,25,38,39,40,79,80,81,83,84,85,87,88] #linux config


class Anode_Win(tk.Frame):
    #saves img that is being used as global, so it doesn't get garbage collected
    #initialize shown
    global img
    img = ImageTk.PhotoImage(server.outimg)
    #init key detection
    keybinds = KeyHandleGroup()
    #makes the label the image is shown in
    def mklabel(self):
        self.lab= tk.Label(rt,image=img)
        self.lab.pack()
        print(self.lab)
        return self.lab
    #refresh function
    def refr(self):
        global img
        #Get shown refreshed
        img = ImageTk.PhotoImage(server.outimg)
        self.lab.configure(image=img) #set lab to new shown #TODO Check if needed
        self.master.after(rft,self.refr) #Schedule new refresh
    #event loop start
    def start(self):
        self.master.after(rft,self.refr) #Schedule first refresh
        self.keybinds()
        self.master.mainloop()
    #initialization of binds
    def keybinds(self):
        #Additional anode keybinds go here:
        #-=---------=-
        for i in CATHkey: #adding cathode keys
            keygroup.addKey(KeyHandle(i))
        print(keygroup.keys)
        #binding keygroup to proper events
        self.bind_all('<KeyPress>', keygroup.onKeyDown)
        self.bind_all('<KeyRelease>' , keygroup.onKeyUp)
        #TODO Learn Tkinter events better, this KeyHandle solution might be unnecessary

    #initialization
    def __init__(self,master=rt):
        tk.Frame.__init__(self,master)
        self.pack()
        self.mklabel()

if __name__ == "__main__":
    w=Anode_Win() #make Anode_Win instance
    s = threading.Thread(target=server.start)
    s.start() #start Anode_Server
    print('starting GUI')
    w.start() #start Anode_Win
