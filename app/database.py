from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ
#import time
#import psycopg2
#from psycopg2.extras import RealDictCursor

SQLALCHEMY_DATABASE_URL = environ.get('SQLALCHEMY_DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() :
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
while True:
    try:
        cnx = psycopg2.connect(user='newuser', password= 'newpassword', 
                                host='127.0.0.1', database= 'fastapi', 
                                cursor_factory = RealDictCursor )
        cursor = cnx.cursor()
        print("database connection was succesful!")
        break
    except Exception as error:
        print("connecting to database failed")
        print("error", error)
        time.sleep(2)
'''