# from polls.models.question import Question
# from polls.models.choice import Choice
# from polls.models.database import SessionLocal

# session = SessionLocal()
# questions = session.query(Question).all()
# for q in questions:
#     print(q.question_text)


from polls.models.database import SessionLocal
from polls.models.question import Question

session = SessionLocal()
questions = session.query(Question).all()

for q in questions:
    print(q.id, q.question_text, q.pub_date)


