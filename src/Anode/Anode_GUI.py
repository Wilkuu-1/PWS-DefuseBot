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

#wrapper for sending control signals to CATHODE
def sig(message,func=0):
    server.sigs.append((message,func)):

class Anode_Win(tk.Frame):
    #saves img that is being used as global, so it doesn't get garbage collected
    #initialize shown
    global imgs
    imgs = [ImageTk.PhotoImage(Image.fromarray(server.outarray,mode='RGB'))]
    #makes the label the image is shown in
    def mklabel(self):
        self.lab= tk.Label(rt,image=imgs[0])
        self.lab.pack()
        print(self.lab)
        return self.lab
    #refresh function
    def refr(self):
        global img
        #Get shown refreshed
        imgs[0] = ImageTk.PhotoImage(Image.fromarray(server.outarray,mode='RGB'))
        self.lab.configure(image=imgs[0]) #set lab to new shown #TODO Check if needed
        self.master.after(rft,self.refr) #Schedule new refresh
    #event loop start
    def start(self):
        self.master.after(rft,self.refr) #Schedule first refresh
        self.keybinds()
        self.master.mainloop()
    #initialization of binds
    def keybinds(self):
        #Keybindings
        #self.bind(<key>,server.sender(b'0000')) 
        self.bind('<Down>', lambda: sig(b'0001')) #main motors backward
        self.bind('<Up>',   lambda: sig(b'0002')) #main motors forward
        self.bind('<Left>', lambda: sig(b'0003')) #main motors left
        self.bind('<Right>',lambda: sig(b'0004')) #main motors right
        #TODO add more controls
    #initialization
    def __init__(self,master=rt):
        tk.Frame.__init__(self,master)
        self.pack()
        self.mklabel()

if __name__ == "__main__":
    w=Anode_Win() #make Anode_Win instance
    server.start() #start Anode_Server
    w.start() #start Anode_Win


