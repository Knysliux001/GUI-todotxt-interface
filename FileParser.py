'''
__line start__
done?
'^x '

done with dates? (as per file format specification cannot be a single date)
'^x (?P<completion_date>\d{4}-\d{2}-\d{2}) (?P<creation_date>\d{4}-\d{2}-\d{2}) '

priority?
'^\((?P<priority>[A-Z])\) '

priority and creation_date
'^\((?P<priority>[A-Z])\) (?P<creation_date>\d{4}-\d{2}-\d{2}) '


__anywhere__
contexts?
' (?P<context>@.*?) '

projects?
' (?P<project>\+.*?) '

due date?
' due:(?P<due_date>\d{4}-\d{2}-\d{2}) '
'''
import re
import logging
from sqlalchemy.orm import sessionmaker
from DBInitializer import *

Session = sessionmaker(bind=engine)
session = Session()

class FileParser():
    def __init__(self, file_name="todo.txt"):
        self.file_name = file_name

    def read_input_file(self):
        try:
            with open(self.file_name, 'r') as input_file:
                line_number = 0
                for line in input_file.readlines():
                    line_number += 1
                    line = line.rstrip()  # to remove whitespaces at the end of lines
                    self.parse_line(line, line_number)
                return line_number

        except FileNotFoundError:
            logging.error(f'File {self.file_name} was not found!')
            return 0


    def parse_line(self, line, line_number=0):
        logging.debug(f'Parsing {line_number}')
        if len(line.strip()) == 0:
            logging.warning(f'Empty line skipped on {self.file_name}:{line_number}')
            pass  # ignore empty lines
        else:
            description = line
            done = self.find_done(line)
            self.create_task(description, done)

    def create_task(self, description, done):
        task = Task(description=description, done=done)
        session.add(task)
        session.commit()

    def find_done(self, line):
        done_re = re.compile(r'^x ')
        result = done_re.search(line)
        if result:
            logging.debug(f'Done set to True on {line}')
            return True
        else:
            logging.debug(f'Done set to False on {line}')
            return False

# testing lines:
parser = FileParser("test.txt")
parser.read_input_file()


session.close()