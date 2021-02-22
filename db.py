from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from config import DB_URL

engine = create_engine(DB_URL, encoding='utf-8', max_overflow=0)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
