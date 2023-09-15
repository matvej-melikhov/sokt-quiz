import random
from flask import request, session, abort, redirect, url_for
from app.models import *
from app.config import *

def login_required(function):
    def inner(*args, **kwargs):
        if "user_id" in session:
            return function(*args, **kwargs)
        return abort(401)
    inner.__name__ = function.__name__
    return inner

def game_started(function):
    def inner(*args, **kwargs):
        if GAME_START_TIME <= datetime.datetime.now():
            return function(*args, **kwargs)
        return redirect(url_for("blocker", next=request.endpoint))
    inner.__name__ = function.__name__
    return inner

def admin_required(function):
    def inner(*args, **kwargs):
        user = get_user_from_session()
        if not user:
            return abort(401)
        if user.is_admin:
            return function(*args, **kwargs)
        else:
            return abort(403)
    inner.__name__ = function.__name__
    return inner

def db_add(obj):
    db.session.add(obj)
    db.session.commit()

def get_question_by_id(question_id):
    question = Questions.query.filter_by(id=question_id).first()
    return question

def get_question_by_hash(user, hash):
    question_id = None
    for q_id, q_hash in user.decodes.items():
        if q_hash == hash:
            question_id = q_id
    question = get_question_by_id(question_id) if question_id else None
    return question

def get_user_from_session():
    user_id = session.get("user_id")
    user = Users.query.filter_by(id=user_id).first()
    return user

def is_correct(question: Questions, answer: str):
    return question.answer.lower() == answer.lower()

def generate_decodes():
    question_ids = [question.id for question in Questions.query.order_by(Questions.weight).all()]
    l = list("0123456789abcdefghijklmnopqrstuvwxyz")
    d = dict()
    for i in range(QUESTIONS_AMOUNT):
        d[question_ids[i]] = "".join([random.choice(l) for _ in range(20)])
    return d

def get_answer(user, question, answer, correct):
    # user_answers = pickle.loads(user.answers)
    question_id = question.id
    user_answers = user.answers.copy()
    user_answers[question_id] = {"answer": answer, "is_correct": correct}
    user.answers = user_answers
    if correct:
        user.score += question.weight
    db.session.add(user)
    db.session.commit()
    return question.weight if correct else 0

def get_time_list(seconds):
    hours = str(seconds // 3600).rjust(2, "0")
    minutes = str(seconds % 3600 // 60).rjust(2, "0")
    seconds = str(seconds % 3600 % 60).rjust(2, "0")
    return {
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }

def stop_game_function(user):
    questions = Questions.query.all()
    answers = user.answers.copy()
    for question in questions:
        if question.id not in answers:
            answers[question.id] = {"answer": "", "is_correct": False}
    user.answers = answers
    user.finish_time = datetime.datetime.now()
    db_add(user)