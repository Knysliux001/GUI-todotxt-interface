#Main app window
from tkinter import *
from threading import *


root = Tk()

root.geometry("1000x800")

def loading():
    thread1 = Thread(target=load)
    thread1.start()

def load():
    print("thread1 loading")

def saving():
    thread2 = Thread(target=save)
    thread2.start()

def save():
    print("thread2 saving")

load_button = Button(root, text="Load", command=loading).pack()
save_button = Button(root, text="Save", command=saving).pack()

root.mainloop()