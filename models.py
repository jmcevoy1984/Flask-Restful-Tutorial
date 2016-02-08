from database import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(80))
    done = db.Column(db.Boolean())
    
    def __init__(self, title, description='', done=''):
        self.title = title
        self.description = description
        self.done = done

