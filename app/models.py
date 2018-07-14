from datetime import datetime
from app import db, app
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100))
    pid = db.Column(db.String(100))
    pmt = db.Column(db.String(100))
    dev_lead = db.Column(db.String(100))
    developers = db.Column(db.String(100))
    release = db.Column(db.String(100))
    sprint_schedule = db.Column(db.String(300))
    lpm = db.Column(db.String(100))
    pm = db.Column(db.String(100))
    scrum_master = db.Column(db.String(100))
    se = db.Column(db.String(100))
    notes = db.Column(db.String(10000))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    impact = db.Column(db.String(100))
    readiness_status = db.Column(db.String(100))
    deployment_cr = db.Column(db.String(100))
    user_story_id = db.Column(db.String(100))
    user_story_desc = db.Column(db.String(1000))
    user_story_name = db.Column(db.String(100))
    task_id = db.Column(db.String(100))
    task_name = db.Column(db.String(100))
    task_desc = db.Column(db.String(1000))

    # objects = db.relationship('DbObject', backref='projects')

    def __repr__(self):
        return '<Project {} - {}>'.format(self.pid, self.project_name)


class UserStory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_story_id = db.Column(db.String(100))
    dev_lead = db.Column(db.String(100))
    developers = db.Column(db.String(100))
    sprint = db.Column(db.String(300))
    points = db.Column(db.String(10))
    size = db.Column(db.String(10))
    epic = db.Column(db.String(20))
    story_notes = db.Column(db.String(3000))
    user_story_desc = db.Column(db.String(3000))
    user_story_name = db.Column(db.String(100))
    project_id = db.Column(db.String(100))
    project_name = db.Column(db.String(100))

    def __repr__(self):
        return '<User Story {} - {}>'.format(self.user_story_id, self.user_story_name)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(100))
    dev_lead = db.Column(db.String(100))
    developers = db.Column(db.String(100))
    sprint = db.Column(db.String(300))
    task_name = db.Column(db.String(100))
    task_desc = db.Column(db.String(1000))
    task_hours = db.Column(db.Integer)
    task_notes = db.Column(db.String(2000))
    user_story_id = db.Column(db.String(100))
    project_id = db.Column(db.String(100))
    project_name = db.Column(db.String(100))

    def __repr__(self):
        return '<Task {} - {}>'.format(self.task_id, self.task_name)


class DbObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dm_seq = db.Column(db.String(100))
    data_type = db.Column(db.String(100))
    schema = db.Column(db.String(100))
    db_object = db.Column(db.String(100))
    frequency = db.Column(db.String(100))
    data_provider = db.Column(db.String(100))
    providing_system = db.Column(db.String(100))
    interface = db.Column(db.String(100))
    topic = db.Column(db.String(100))
    data_retention = db.Column(db.String(100))
    latency = db.Column(db.String(100))
    data_in_qa0 = db.Column(db.String(100))
    row_count_per_period = db.Column(db.String(100))
    active_in_prod = db.Column(db.String(100))
    order_by = db.Column(db.String(100))
    segment_by = db.Column(db.String(100))
    special_notes = db.Column(db.String(1000))
    # project_id = db.Column(db.String, db.ForeignKey('project.pid'))
    project_id = db.Column(db.String(100))
    project_name = db.Column(db.String(100))

    def __repr__(self):
        return '<DbObject {}, {}>'.format(self.id, self.dm_seq)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

