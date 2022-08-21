# file change observer test for todo.txt
# no need to check for file creation or deletion
# modified from https://stackoverflow.com/questions/30531477/how-do-i-watch-a-file-not-a-directory-for-changes-using-python

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileModHandler(FileSystemEventHandler):

    def __init__(self, path, file_name, callback):
        self.file_name = file_name
        self.callback = callback

        self.observer = Observer()
        self.observer.schedule(self, path, recursive=False)
        self.observer.start()
        self.observer.join()

    def on_modified(self, event):
        # to filter directory events and other file events
        if not event.is_directory and event.src_path.endswith(self.file_name):
            # self.observer.stop() # stop watching
            self.callback() # call callback


if __name__ == '__main__':

    def callback():
        print("todo.txt was changed")
        # trigger DB reload

    FileModHandler('.', 'todo.txt', callback)