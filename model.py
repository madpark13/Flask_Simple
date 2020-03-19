from datetime import date
from sqlalchemy import (Column, Integer, String, Boolean, Text, Date, 
                        ForeignKey, create_engine)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('sqlite:///app.db', echo=True)
Base = declarative_base(bind=engine)


class AccountExists(Exception):
    '''
    Authentification pair already in db
    '''

class AccountNotFound(Exception):
    '''
    Authentification pair not found in db
    '''

class Abstract:
    id = Column(Integer, primary_key=True)
    created_on = Column(Date, default=date.today())


class User(Abstract, Base):
    __tablename__ = 'users'
    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(60), nullable=False)

    tasks = relationship("Task", cascade="all, delete-orphan")

    def __str__(self):
        return ' | '.join([self.id, self.username, self.email, self.password])


class Task(Abstract, Base):
    __tablename__ = 'tasks'
    title = Column(String(20), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    details = Column(Text)
    deadline = Column(Date)
    status = Column(Boolean, default=0)

    author = relationship(User)

    def __str__(self):
        return ' | '.join([self.id, self.title, self.status])

# Base.metadata.create_all()

def add_user(name, email, password):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = User(username=name, email=email, password=generate_password_hash(password))
    try:
        session.add(user)
        session.commit()
    except IntegrityError:
        raise AccountExists
    finally:
        session.close()


def check_user(email, password):
    
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(email=email).first()
    session.close()
    if not (user and check_password_hash(user.password, password)):
        raise AccountNotFound
    return user.username

def get_user_tasks(name):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(username=name).first()
    try:
        return user.tasks
    except AttributeError:
        raise AccountNotFound
    finally:
        session.close()

def create_user_task(author_id, title, details='', deadline=None):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).get(author_id)
    user_tasks = user.tasks
    if deadline:
        deadline = date.fromisoformat(deadline)
        new_task = Task(title=title, details=details, deadline=deadline)
    else:
        new_task = Task(title=title, details=details)
    user_tasks.append(new_task)
    session.commit()
    session.close()


def change_user_task(username, id):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(username=username).first()
    user_tasks = user.tasks
    task_to_change = user_tasks[id-1]
    task_to_change.status = not(task_to_change.status)
    session.commit()
    session.close()

def remove_user_task(username, id):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(username=username).first()
    task_to_remove = user.tasks[id-1]
    session.delete(task_to_remove)
    session.commit()

def get_id_by_name(name):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(username=name).first()
    session.close()
    try:   
        return user.id
    except AttributeError:
        raise AccountNotFound