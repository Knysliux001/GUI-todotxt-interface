# Main app window
import contextvars
from tkinter import *
from threading import *
import time
import logging
import sys
from db_initializer import *
from db_interface import *
from file_parser import FileParser



# logging.basicConfig(filename='guiapp.log', level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
Base.metadata.drop_all(bind=engine, checkfirst=True)
Base.metadata.create_all(engine)


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
    status_label["text"] = "parsing the file..."
    parser = FileParser("test.txt")
    Base.metadata.drop_all(bind=engine, checkfirst=True)
    Base.metadata.create_all(engine)
    status = parser.digest_input_file()
    if status != 0:
        pass  # actions for filenotfound
    status_label["text"] = "Finished parsing"
    status_label["text"] = "loading..."
    context_listbox.delete(0, END)
    context_listbox.insert(END, "")
    for context_obj in session.query(Context).order_by(Context.context).all():
        context_listbox.insert(END, context_obj)
    project_listbox.delete(0, END)
    project_listbox.insert(END, "")
    for project_obj in session.query(Project).order_by(Project.project).all():
        project_listbox.insert(END, project_obj)
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
context_listbox.pack(side=TOP, fill=Y)

project_listbox = Listbox(filters_frame)
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

root.after(0, loading)
root.mainloop()

