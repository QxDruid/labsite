from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Slider_image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Index = db.Column(db.Integer,index=True)
    Image = db.Column(db.String(32))

    def __repr__(self):
        return '<index: {}, img: {}>'.format(self.Index, self.Image)

    @staticmethod
    def delete_image(index):
        base = Slider_image.query.filter_by(Index = index).first()
        if base:
            db.session.delete(base)
            db.session.commit()
            return True
        return False

    @staticmethod
    def set_image(index, image):
        base = Slider_image.query.filter_by(Index = index).first()
        if base:
            base.Image = image
        else:
            base = Slider_image.query.order_by(Slider_image.Index.desc()).first()
            if base and index > base.Index:
                index = base.Index + 1
            base = Slider_image()
            base.Image = image
            base.Index = index
            db.session.add(base)
        db.session.commit()

class News(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Image = db.Column(db.String(128))
    Title = db.Column(db.String(128), index=True, unique=True)
    Description = db.Column(db.String(256))
    Fulltext = db.Column(db.String)

    def __repr__(self):
        return '<Id: {}, Title: {}>'.format(self.id, self.Title)

    @staticmethod
    def set_news(image, title, description, fulltext):
        news = News()
        news.Description = description
        news.Title = title
        news.Fulltext = fulltext
        if image:
            news.Image = image
        db.session.add(news)
        db.session.commit()
    
    @staticmethod
    def edit_news(id, image, title, description, fulltext):
        news = News.query.get(id)
        news.Image = image
        news.Title = title
        news.Description = description
        news.Fulltext = fulltext

        db.session.add(news)
        db.session.commit()




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

    @staticmethod
    def set_person(name, secondName, middleName, position, info, image):
        pers = Person()
        pers.FirstName = name
        pers.SecondName = secondName
        pers.MiddleName = middleName
        pers.Position = position
        pers.Info = info
        pers.Image = image
        db.session.add(pers)
        db.session.commit()

    @staticmethod
    def del_person(pers):
        db.session.delete(pers)
        db.session.commit()

    @staticmethod
    def edit_person(id, name, secondName, middleName, position, info, image):
        pass
    
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


class Publication(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Year = db.Column(db.Integer)
    Text = db.Column(db.String)
    DOI = db.Column(db.String, index = True)

class Patent(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Text = db.Column(db.String)

class Project(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Text = db.Column(db.String)


class Gallery_image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Image = db.Column(db.String(32))
    Description = db.Column(db.String)
    
    @staticmethod
    def delete_image(id):
        base = Gallery_image.query.filter_by(id = id).first()
        if base:
            db.session.delete(base)
            db.session.commit()
            return True
        return False

    @staticmethod
    def set_image(image, description):
        base = Gallery_image()
        base.Image = image
        base.Description = description
        db.session.add(base)
        db.session.commit()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
