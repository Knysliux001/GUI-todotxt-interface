from db_initializer import *
from datetime import datetime
# from file_parser import FileParser
import logging
import sys
from sqlalchemy.orm import sessionmaker

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)

Session = sessionmaker(bind=engine)
session = Session()


class DBInterface():
    def __init__(self, ses):
        self.session = ses

    def add_task(self, parsed_line):
        # empty?
        if not parsed_line:
            logging.error(f'DBInterface.add_task received an empty task!')
            return 1
        # duplicate?
        dupl_task = self.session.query(Task).filter(Task.description == parsed_line["description"]).first()
        if dupl_task:
            logging.warning(f'Duplicate task: {dupl_task=}')
            return 2
        task = Task(description=parsed_line["description"],
                    done=parsed_line["done"],
                    priority=parsed_line["priority"],
                    # creation_date=parsed_line["creation_date"],
                    # completion_date=parsed_line["completion_date"],
                    # due_date=parsed_line["due_date"]
                    )
        if parsed_line["creation_date"]:
            task.creation_date = datetime.strptime(parsed_line["creation_date"], '%Y-%m-%d').date()
            logging.debug(f'{parsed_line["creation_date"]=}')
        if parsed_line["completion_date"]:
            task.completion_date = datetime.strptime(parsed_line["completion_date"], '%Y-%m-%d').date()
            logging.debug(f'{parsed_line["completion_date"]=}')
        if parsed_line["due_date"]:
            task.due_date = datetime.strptime(parsed_line["due_date"], '%Y-%m-%d').date()
            logging.debug(f'{parsed_line["due_date"]=}')
        self.session.add(task)
        self.session.commit()
        if parsed_line["contexts"]:
            for context in parsed_line["contexts"]:
                logging.debug(f'Working on: {context=}')
                # existing context?
                existing_context = None
                existing_context = self.session.query(Context).filter(Context.context == context).first()
                if existing_context:
                    logging.debug(f'Existing context found: {existing_context=}')
                    task.contexts.append(existing_context)
                    self.session.commit()
                    logging.debug(f'commit on {existing_context=} worked!')
                else:
                    logging.debug(f'New context found: {context=}')
                    task.contexts.append(Context(context=context))
                    self.session.commit()
                    logging.debug(f'commit on {context=} worked!')
        else:
            logging.debug('No contexts')
        if parsed_line["projects"]:
            for project in parsed_line["projects"]:
                logging.debug(f'Working on: {project=}')
                # existing project?
                existing_project = None
                existing_project = self.session.query(Project).filter(Project.project == project).first()
                if existing_project:
                    logging.debug(f'Existing project found: {existing_project=}')
                    task.projects.append(existing_project)
                    self.session.commit()
                    logging.debug(f'commit on {existing_project=} worked!')
                else:
                    logging.debug(f'New project found: {project=}')
                    task.projects.append(Project(project=project))
                    self.session.commit()
                    logging.debug(f'commit on {project=} worked!')
        else:
            logging.debug('No projects')
        return 0



# testing lines:
if __name__ == "__main__":
    parsed_line1 = {'description': '(A) 2012-12-10 Email to 0 @work @pc due:2012-12-12 +email +bigproject', 'done': False, 'completion_date': None, 'priority': 'A', 'creation_date': '2012-12-10', 'contexts': ['@work', '@pc'], 'projects': ['+email', '+bigproject'], 'due_date': '2012-12-12'}
    parsed_line2 = {'description': '(B) 2012-12-12 Call boss about that +bigproject @work @phone +bigproject', 'done': False, 'completion_date': None, 'priority': 'B', 'creation_date': '2012-12-10', 'contexts': ['@work', '@phone'], 'projects': ['+bigproject'], 'due_date': None}

    db_interface = DBInterface(session)
    Base.metadata.drop_all(bind=engine, checkfirst=True)
    Base.metadata.create_all(engine)
    db_interface.add_task(parsed_line1)
    db_interface.add_task(parsed_line2)

    # session.close()
