from app import db

class Entries(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64),index=True)
    text = db.Column(db.String, index=True)

    def __repr__(self):
        return '<title: {}, text: {}>'.format(self.title, self.text)
