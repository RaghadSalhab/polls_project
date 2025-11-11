import pymysql
import psycopg2  
import os

from polls.models.request_scope import get_current_request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

#DATABASE_URL = "mysql+pymysql://root:1234@127.0.0.1:3306/polls_db"
#DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/polls_db"
# DATABASE_URL = "postgresql+psycopg2://postgres:1234@host.docker.internal:5432/polls_db"
if os.environ.get("DOCKER_DISABLED") == "1":
    DATABASE_URL = "postgresql+psycopg2://postgres:1234@127.0.0.1:5432/polls_db_local"
else:
    # DATABASE_URL = "postgresql+psycopg2://postgres:1234@host.docker.internal:5432/polls_db"
    DATABASE_URL = "mysql+pymysql://local_user:local_pass@mysql_local:3306/polls_db"

engine = create_engine(DATABASE_URL, echo=False)
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(SessionFactory,scopefunc=get_current_request)  
ConsumerSession = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()
# Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    try:
        conn = engine.connect()
        print("Connection successful!")
        conn.close()
    except Exception as e:
        print("Connection failed:", e)


