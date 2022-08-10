# Main app window
from tkinter import *
from threading import *
import time
import logging
import sys
from db_initializer import *
from file_parser import FileParser



# logging.basicConfig(filename='guiapp.log', level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

Base.metadata.create_all(engine)

parser = FileParser("test.txt")
parser.read_input_file()


root = Tk()
# window geometry definitions
root.title('todo.txt interpreter')
top_frame = Frame(root)
filters_frame = Frame(root)
tasks_frame = Frame(root)
status_frame = Frame(root)


def loading():
    thread1 = Thread(target=load)
    thread1.start()


def load():
    logging.debug("thread1 loading")
    status_label["text"] = "thread1 is loading..."
    time.sleep(1)
    status_label["text"] = "Idle"


def saving():
    thread2 = Thread(target=save)
    thread2.start()


def save():
    logging.debug("thread2 saving")
    status_label["text"] = "thread2 is saving..."
    time.sleep(1)
    status_label["text"] = "Idle"


load_button = Button(top_frame, text="Load", command=loading)
load_button.pack(side=LEFT)
save_button = Button(top_frame, text="Save", command=saving)
save_button.pack(side=LEFT)

context_listbox = Listbox(filters_frame)
context_listbox.insert(END, "@test_context")
context_listbox.pack(side=TOP, fill=Y)

project_listbox = Listbox(filters_frame)
project_listbox.insert(END, "+test_project")
project_listbox.pack(side=BOTTOM, fill=Y)

task_listbox = Listbox(tasks_frame, height=20, width=70)
task_listbox.insert(END, "some_task from @test_context in +test_project")
task_listbox.pack(fill=BOTH)

status_label = Label(status_frame, text="Idle", bd=1, relief=SUNKEN, anchor=W)
status_label.pack(side=BOTTOM, fill=X)

top_frame.pack(side=TOP, fill=X)
status_frame.pack(side=BOTTOM, fill=X)  # must be before others!
filters_frame.pack(side=LEFT, fill=Y)
tasks_frame.pack(side=RIGHT, fill=BOTH)

root.mainloop()

