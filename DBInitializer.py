import datetime
from sqlalchemy import Column, Boolean, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///internaltest.db')
Base = declarative_base()


class InternalDB(Base):
    __tablename__ = 'Tasks'
    id = Column(Integer, primary_key=True, nullable=False)
    description = Column("Description", String, nullable=False) #whole line
    done = Column("Done", Boolean, nullable=False)
    creation_date = Column("Creation date", Date, nullable=True, default=None)
    completion_date = Column("Completion date", Date, nullable=True, default=None)
    due_date = Column("Due date", Date, nullable=True, default=None)
    priority = Column("Priority", String(1), nullable=True, default=None)
    # hidden = Column("Hidden", Boolean, nullable=False, default=None)

    def __init__(self, description, done):
        self.description = description
        self.done = done

    def __repr__(self):
        return f"{self.description}"

Base.metadata.create_all(engine)