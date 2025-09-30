# from polls.models.database import Base, engine
# from polls.models.user import User   # استورد الموديل هنا فقط

# # ينشئ كل الجداول
# Base.metadata.create_all(bind=engine)
# print("Tables created successfully!")


# init_db.py
from polls.models.database import Base, engine
from polls.models.question import Question
from polls.models.choice import Choice

Base.metadata.create_all(bind=engine)

print("Tables are ready!")
