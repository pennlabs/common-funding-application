from app.models import Question

QUESTIONS = [
    "Is your event primarily a speaker event (i.e. over 50% speaking)?",
    "If your event features a speaker or performance, does it include any kind of interactive components?",
    "Is alcohol served at your event?",
    "Is your event a closed event?",
    "Does your event serve minority interests on campus?",
]

def import_questions():
    Question.objects.all().delete()
    for question in QUESTIONS:
        Question.objects.create(question=question)
