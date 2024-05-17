from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


URL_DATABASE = 'mysql+pymysql://VS-CODE:vscode@localhost:3306/workout'

engine = create_engine(URL_DATABASE)

sessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

