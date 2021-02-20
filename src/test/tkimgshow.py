import tkinter as tk
from PIL import ImageTk, Image
import time
import numpy as np

rt = tk.Tk()
class Window(tk.Frame):
    global imgs
    imgs = [Image.open("dog.jpg"),Image.open("cat.jpg")]
    def mklabel(self):
        self.L = tk.Label(self.master,image=ImageTk.PhotoImage(imgs[1]))
        self.L.pack()
        print(self.L)
        return self.L
    #Called every x miliseconds
    def refr(self,n):
        global img
        #imgs must be recalled bc tk or smth 
        img = ImageTk.PhotoImage(imgs[n])
        self.L.configure(image=img)
        print(f"refreshed to {n}")
        if n:
            n=0
        else:
            n=1
        rt.after(1000,lambda: self.refr(n))
    def start(self):
        rt.after(1000,lambda: self.refr(0))
        rt.mainloop()
    def __init__(self,master = None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.mklabel()
 
w = Window()
w.start()
