import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

DATABASE_URL = "mysql+pymysql://root:1234@127.0.0.1:3306/polls_db"

engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(SessionFactory)  
Base = declarative_base()
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    try:
        conn = engine.connect()
        print("Connection successful!")
        conn.close()
    except Exception as e:
        print("Connection failed:", e)
