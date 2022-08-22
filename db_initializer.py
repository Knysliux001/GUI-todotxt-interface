from sqlalchemy import Table, ForeignKey, Column, Boolean, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite://',
connect_args={'check_same_thread': False}
)
Base = declarative_base()

task_context = Table(
    "task_context",
    Base.metadata,
    Column("task_id", ForeignKey("Task.id"), primary_key=True),
    Column("context_id", ForeignKey("Context.id"), primary_key=True)
)

task_project = Table(
    "task_project",
    Base.metadata,
    Column("task_id", ForeignKey("Task.id"), primary_key=True),
    Column("project_id", ForeignKey("Project.id"), primary_key=True)
)


class Task(Base):
    __tablename__ = 'Task'
    id = Column(Integer, primary_key=True)
    description = Column("Description", String, nullable=False, unique=True)  # decided to never allow duplicates
    done = Column("Done", Boolean, nullable=False)
    creation_date = Column("Creation date", Date, nullable=True, default=None)
    completion_date = Column("Completion date", Date, nullable=True, default=None)
    due_date = Column("Due date", Date, nullable=True, default=None)
    priority = Column("Priority", String(1), nullable=True, default=None)
    contexts = relationship("Context", secondary=task_context)
    projects = relationship("Project", secondary=task_project)

    def __repr__(self):
        return f"{self.description}"

    def clear(self):
        self.id = None
        self.description = None
        self.done = None
        self.creation_date = None
        self.completion_date = None
        self.due_date = None
        self.priority = None
        return self


class Context(Base):
    __tablename__ = 'Context'
    id = Column(Integer, primary_key=True)
    context = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"{self.context}"

    def clear(self):
        self.id = None
        self.context = None
        return self


class Project(Base):
    __tablename__ = 'Project'
    id = Column(Integer, primary_key=True)
    project = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"{self.project}"

    def clear(self):
        self.id = None
        self.project = None
        return self

Base.metadata.create_all(engine)
