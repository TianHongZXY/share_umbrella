from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    wx = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), index=True)
    # 男1，女0
    sex = db.Column(db.Integer, default=1)
    success_counts = db.Column(db.Integer, default=0)
    neednotes = db.relationship('NeedNotes')
    offernotes = db.relationship('OfferNotes')
    avatarurl = db.Column

    def __repr__(self):
        return '<User %r>' % self.username

class NeedNotes(db.Model):
    __tablename__ = 'neednotes'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) # 还得加上有效期时间
    helper = db.Column(db.String())

    def __init__(self, content=content, user_id=user_id):
        content = content
        user_id = user_id
        is_active = True

class OfferNotes(db.Model):
    __tablename__ = 'offernotes'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_active = db.Column(db.Boolean, default=True)
    helped = db.Column(db.Integer, ForeignKey='users')
    def __init__(self, content=content, author_wx=author_wx):
        content = content
        author_wx = author_wx
        is_active = True

@login_manager.user_loader
def load_user(student_id):
    return User.query.get(int(student_id))


