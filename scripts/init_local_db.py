#scripts/init_local_db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

os.environ["DOCKER_DISABLED"] = "1"

DATABASE_URL_LOCAL = "postgresql+psycopg2://postgres:1234@127.0.0.1:5432/polls_db_local"
local_engine = create_engine(DATABASE_URL_LOCAL, echo=False)
LocalSession = sessionmaker(bind=local_engine, expire_on_commit=False)
Base = declarative_base()

def create_local_schema():
    try:
        conn_local = local_engine.connect()
        print("✅ Connection to Local DB successful!")
        conn_local.close()

        from polls.models import user, question, choice

        Base.metadata.create_all(bind=local_engine)
        print("✅ Tables created successfully on Local DB!")

    except Exception as e:
        print("❌ Connection or schema creation failed:", e)

if __name__ == "__main__":
    create_local_schema()
