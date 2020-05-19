from app import db

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))


    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email