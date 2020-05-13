from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Slider_image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Index = db.Column(db.Integer,index=True)
    Image = db.Column(db.String(32))

    def __repr__(self):
        return '<index: {}, img: {}>'.format(self.index, self.img)

    @staticmethod
    def delete_image(index):
        base = Slider_image.query.filter_by(index = index).first()
        if base:
            db.session.delete(base)
            db.session.commit()
            return True
        return False

    @staticmethod
    def set_image(index, image):
        base = Slider_image.query.filter_by(index = index).first()
        if base:
            base.img = image
        else:
            base = Slider_image.query.order_by(Slider_image.index.desc()).first()
            if base and index > base.index:
                index = base.index + 1
            base = Slider_image()
            base.img = image
            base.index = index
            db.session.add(base)
        db.session.commit()

class News(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Image = db.Column(db.String(32))
    Title = db.Column(db.String(32), index=True)
    Description = db.Column(db.String(256))
    Fulltext = db.Column(db.String)

    def __repr__(self):
        return '<Id: {}, Title: {}>'.format(self.id, self.Title)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    FirstName = db.Column(db.String(32))
    SecondName = db.Column(db.String(32))
    MiddleName = db.Column(db.String(32))
    Image = db.Column(db.String(32))
    Position = db.Column(db.String(32))
    Info = db.Column(db.String)

    def __repr__(self):
        return '<Id: {}, Fullname: {}>'.format(self.id, self.FirstName + self.MiddleName + self.SecondName)

class Research(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Image = db.Column(db.String(32))
    Title = db.Column(db.String(32), index=True)
    Description = db.Column(db.String)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))