'''
__line start__
done?
'^x '

done with dates? (as per file format specification cannot be a single date)
'^x (?P<completion_date>\d{4}-\d{2}-\d{2}) (?P<creation_date>\d{4}-\d{2}-\d{2}) '

priority?
'^\((?P<priority>[A-Z])\) '

priority and creation_date?
'^\((?P<priority>[A-Z])\) (?P<creation_date>\d{4}-\d{2}-\d{2}) '

no priority, creation_date?
'^(?P<creation_date>^\d{4}-\d{2}-\d{2}) '

__anywhere__
contexts?
'(?P<context>@\S*)'

projects?
'(?P<project>\+\S*)'

due date?
'due:(?P<due_date>\d{4}-\d{2}-\d{2})'
'''
import re
import logging
import sys
from sqlalchemy.orm import sessionmaker
from db_initializer import *
# from datetime import date

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

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
                    parsed_line = self.parse_line(line, line_number)
                return line_number

        except FileNotFoundError:
            logging.error(f'File {self.file_name} was not found!')
            return 0


    def parse_line(self, line, line_number=0):
        logging.debug(f'Parsing {line_number=}')
        parsed_line = {}
        if len(line.strip()) == 0:
            logging.warning(f'Empty line skipped on {self.file_name}:{line_number}')
            pass  # ignore empty lines
        else:
            parsed_line["description"] = line
            parsed_line["done"] = self.find_done(line)
            logging.debug(f'{parsed_line["done"]=} {parsed_line["description"]}')
            if parsed_line["done"]:
                parsed_line["creation_date"], parsed_line["completion_date"] = self.find_done_dates(line)
                logging.debug(f'{parsed_line["creation_date"]=} {parsed_line["completion_date"]=} {parsed_line["description"]}')
            else:
                parsed_line["priority"] = self.find_priority(line)
                if parsed_line["priority"]:
                    parsed_line["creation_date"] = self.find_priority_creation_date(line)
                else:
                    parsed_line["creation_date"] = self.find_creation_date(line)
            parsed_line["contexts"] = self.find_contexts(line)
            parsed_line["projects"] = self.find_projects(line)
            parsed_line["due_date"] = self.find_due_date(line)
        logging.debug(f'{parsed_line=}')
        return parsed_line

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

    def find_done_dates(self, line):
        done_dates_re = re.compile(r'^x (?P<completion_date>\d{4}-\d{2}-\d{2}) (?P<creation_date>\d{4}-\d{2}-\d{2}) ')
        result = done_dates_re.search(line)
        if result:
            creation_date = (result.group('creation_date'))
            completion_date = (result.group('completion_date'))
            logging.debug(f'Done dates set to {creation_date=} {completion_date=}')
            return creation_date, completion_date
        else:
            return None, None


    def find_priority(self, line):
        priority_re = re.compile(r'^\((?P<priority>[A-Z])\) ')
        result = priority_re.search(line)
        if result:
            priority = result.group('priority')
            logging.debug(f'Priority set to {priority=} on {line}')
            return priority
        else:
            logging.debug(f'No priority on {line}')
            return None

    def find_priority_creation_date(self, line):
        priority_date_re = re.compile(r'^\((?P<priority>[A-Z])\) (?P<creation_date>\d{4}-\d{2}-\d{2}) ')
        result = priority_date_re.search(line)
        if result:
            creation_date = result.group('creation_date')
            logging.debug(f'Creation date set to {creation_date=} on {line}')
            return creation_date
        else:
            return None

    def find_creation_date(self, line):
        creation_date_re = re.compile(r'^(?P<creation_date>^\d{4}-\d{2}-\d{2}) ')
        result = creation_date_re.search(line)
        if result:
            creation_date = result.group('creation_date')
            logging.debug(f'Creation date set to {creation_date=} on {line}')
            return creation_date
        else:
            return None

    def find_contexts(self, line):
        contexts_re = re.compile(r'(?P<context>@\S*)')
        results = contexts_re.findall(line)
        if results:
            logging.debug(f'Found {results} contexts in {line}')
            return results
        else:
            return None

    def find_projects(self, line):
        projects_re = re.compile(r'(?P<project>\+\S*)')
        results = projects_re.findall(line)
        if results:
            logging.debug(f'Found {results} projects in {line}')
            return results
        else:
            return None

    def find_due_date(self, line):
        due_date_re = re.compile(r'due:(?P<due_date>\d{4}-\d{2}-\d{2})')
        result = due_date_re.search(line)
        if result:
            due_date = result.group('due_date')
            logging.debug(f'Due date set to {due_date=} on {line}')
            return due_date
        else:
            return None


# testing lines:
parser = FileParser("test.txt")
parser.read_input_file()


session.close()