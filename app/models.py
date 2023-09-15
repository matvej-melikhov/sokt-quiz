from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    faculty = db.Column(db.String(50))
    group = db.Column(db.Integer())
    registration_time = db.Column(db.PickleType()) # datetime.datetime
    finish_time = db.Column(db.PickleType()) # datetime.datetime
    is_admin = db.Column(db.Integer()) # 0 or 1

    score = db.Column(db.Integer())

    answers = db.Column(db.PickleType()) # dict
    decodes = db.Column(db.PickleType()) # dict with decode id questions

    def __repr__(self):
        return f"Пользователь {self.name}"

class Questions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(300))
    options = db.Column(db.PickleType()) # list
    answer = db.Column(db.String(50))
    weight = db.Column(db.Integer())
    category = db.Column(db.String(300))

    def __repr__(self):
        return f"Вопрос {self.id}"