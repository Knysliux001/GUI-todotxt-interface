# Main app window
import contextvars
from tkinter import *
import tkinter.simpledialog, tkinter.filedialog
from threading import *
import time
import logging
import sys
from db_initializer import *
from db_interface import DBInterface, session
from file_parser import FileParser
from datetime import date


# logging.basicConfig(filename='guiapp.log', level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
Base.metadata.drop_all(bind=engine, checkfirst=True)
Base.metadata.create_all(engine)

TODO_FILE = "todo.txt"

block = 0

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
    parser = FileParser(TODO_FILE)
    # Base.metadata.drop_all(bind=engine, checkfirst=True)
    Base.metadata.create_all(engine)
    status = parser.digest_input_file()
    if status != 0:
        pass  # actions for filenotfound
    status_label["text"] = "Finished parsing"
    status_label["text"] = "loading..."
    context_listbox.delete(0, END)
    context_listbox.insert(END, "")
    context_listbox.insert(END, "-")
    for context_obj in session.query(Context).order_by(Context.context).all():
        context_listbox.insert(END, context_obj)
    project_listbox.delete(0, END)
    project_listbox.insert(END, "")
    for project_obj in session.query(Project).order_by(Project.project).all():
        project_listbox.insert(END, project_obj)
    task_listbox.delete(0, END)
    for task_obj in session.query(Task).order_by(Task.done.asc(),Task.priority.desc(),Task.due_date.desc()).all():
        task_listbox.insert(END, task_obj)
    status_label["text"] = "Idle"


def new_task():
    def add(event=None):
        task_str = entry.get()
        task_str = task_str.rstrip()
        if len(task_str) == 0:
            logging.error(f'Empty task, cannot add.')
            status_label["text"] = "Cannot add empty task"
            return
        task_listbox.insert(END, task_str)
        with open(TODO_FILE, "a") as append_file:
            append_file.write(f'\n{task_str}')
        newWindow.destroy()
        load()

    newWindow = Toplevel(root)
    newWindow.title("Add task")
    entry = Entry(newWindow, width=100)
    entry.pack(side=LEFT, fill=X)
    entry.focus()

    task_str = ""
    newWindow.bind("<Escape>", lambda x: newWindow.destroy())
    newWindow.bind("<Return>", add)
    cancel_button = Button(newWindow, text="Cancel", command=newWindow.destroy)
    cancel_button.pack(side=RIGHT)
    add_button = Button(newWindow, text="Add", textvariable=task_str, command=add)
    add_button.pack(side=RIGHT)

def done_task():
    done_sel = task_listbox.get(ANCHOR)
    logging.debug(done_sel)
    if not done_sel:
        logging.warning(f'Nothing has been selected!')
        status_label["text"] = "No selection!"
        return
    if done_sel.startswith('x '):
        logging.warning(f'The task {done_sel} is already done!')
        status_label["text"] = "Already done!"
        return
    else:
        done_task_obj = session.query(Task).filter(Task.description == done_sel).first()
        done_task_obj.done = True
        done_task_obj.description = 'x ' + done_task_obj.description
        if done_task_obj.priority:
            done_task_obj.priority = None
        if done_task_obj.creation_date:
            done_task_obj.completion_date = date.today()
        logging.debug(f'{vars(done_task_obj)}')
        session.commit()
        # # delete and save here
        with open(TODO_FILE, "r+") as edit_file:
            data = edit_file.readlines()
            edit_file.seek(0)
            for line in data:
                if line.rstrip() != done_sel:
                    edit_file.write(line)
                else:
                    logging.debug(f'{done_sel} removed')
            edit_file.truncate()
        with open(TODO_FILE, "a") as append_file:
            append_file.write(f'\nx {done_sel}')
        load()

def on_context_select(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        context_sel = event.widget.get(index)
        logging.debug(f'{context_sel=}')
        if context_sel == "-":
            task_listbox.delete(0, END)
            for task_obj in session.query(Task).filter(~Task.contexts.any()).order_by(Task.done.asc(), Task.priority.desc(),
                                                         Task.due_date.desc()).all():
                task_listbox.insert(END, task_obj)
            status_label["text"] = "Filtering..."
            return
        if not context_sel:
            task_listbox.delete(0, END)
            for task_obj in session.query(Task).order_by(Task.done.asc(), Task.priority.desc(),
                                                         Task.due_date.desc()).all():
                task_listbox.insert(END, task_obj)
            status_label["text"] = "Idle"
        else:
            task_listbox.delete(0, END)
            for task_obj in session.query(Task).filter(Task.contexts.any(Context.context == context_sel)).order_by(
                    Task.done.asc(), Task.priority.desc(),
                    Task.due_date.desc()).all():
                task_listbox.insert(END, task_obj)
            status_label["text"] = "Filtering..."


def on_project_select(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        project_sel = event.widget.get(index)
        logging.debug(f'{project_sel=}')
        if not project_sel:
            task_listbox.delete(0, END)
            for task_obj in session.query(Task).order_by(Task.done.asc(), Task.priority.desc(),
                                                         Task.due_date.desc()).all():
                task_listbox.insert(END, task_obj)
            status_label["text"] = "Idle"
        else:
            task_listbox.delete(0, END)
            for task_obj in session.query(Task).filter(Task.projects.any(Project.project == project_sel)).order_by(
                    Task.done.asc(), Task.priority.desc(),
                    Task.due_date.desc()).all():
                task_listbox.insert(END, task_obj)
            status_label["text"] = "Filtering..."


load_button = Button(top_frame, text="Load", command=loading)
load_button.pack(side=LEFT)

done_button = Button(top_frame, text="Done", command=done_task)
done_button.pack(side=RIGHT)
new_button = Button(top_frame, text="New", command=new_task)
new_button.pack(side=RIGHT)

context_listbox = Listbox(filters_frame)
context_listbox.pack(side=TOP, fill=BOTH, expand=True)
context_listbox.bind("<<ListboxSelect>>", on_context_select)

project_listbox = Listbox(filters_frame)
project_listbox.pack(side=BOTTOM, fill=BOTH, expand=True)
project_listbox.bind("<<ListboxSelect>>", on_project_select)

task_scroll = Scrollbar(tasks_frame, orient=VERTICAL)

task_listbox = Listbox(tasks_frame, height=20, width=100, yscrollcommand=task_scroll.set)
task_scroll.config(command=task_listbox.yview)
task_scroll.pack(side=RIGHT, fill=Y)
task_listbox.pack(fill=BOTH, expand=True)

status_label = Label(status_frame, text="Idle", bd=1, relief=SUNKEN, anchor=W)
status_label.pack(side=BOTTOM, fill=X)

top_frame.pack(side=TOP, fill=X)
status_frame.pack(side=BOTTOM, fill=X)  # must be before others!
filters_frame.pack(side=LEFT, fill=BOTH, expand=True)
tasks_frame.pack(side=RIGHT, fill=BOTH, expand=True)

root.after(0, loading)
root.mainloop()
