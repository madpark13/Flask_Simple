# import model
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import Session
from model import Base, add_user, create_user_task
import json
# import os
from flask.cli import FlaskGroup 
from app import app

cli = FlaskGroup(app)

@cli.command('reset-db')
def reset_db():
#     os.remove('app.db')
#     engine = create_engine('sqlite:///app.db', echo=True)
    # session = Session(bind=engine)
    # session.query(User).delete()
    # session.commit()
    # print(dir(Base.metadata))
    Base.metadata.drop_all()
    Base.metadata.create_all()

@cli.command('fill-users')
def fill_users():
    with open('MOCK_DATA.json') as f:
        mock = json.load(f)
    for i in mock:
        add_user(**i)
        # add_user(name=i['name'], 
        # email=i['email'], 
        # password=i['password'])


@cli.command('fill-tasks')
def fill_tasks():
    with open('MOCK_DATA_TASKS.json') as f:
        mock = json.load(f)
    for i in mock:
        create_user_task(**i)

cli()
# reset_db()
# fill_db()