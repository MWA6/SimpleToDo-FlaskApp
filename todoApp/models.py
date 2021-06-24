from todoApp import db, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    notes = db.relationship('NotesDB', backref='creator', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.password}')"


class NotesDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    done = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"NotesDB('{self.notes}', '{self.user_id}')"
