#!flask/bin/python
import unittest

from flask_login import login_user,current_user
from flask import session
from app import create_app
from app.admin.routes import response
from config import Config
from app import db
from app.db_models import News, User
from app.forms import AddNewsForm
from io import BytesIO
import os

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class=Config)
        self.app.app_context().push()
        self.client = self.app.test_client()

        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
        u =  User(username = 'James', admin = True)
        u.set_password('007')
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_non_auth(self):
        response = self.client.get("/admin")
        self.assertEqual(response.status, "401 UNAUTHORIZED")

    def test_auth(self):

        user = User.query.filter_by(username='James').first()
        self.assertTrue(user.check_password('007'))

        with self.client:
            self.client.post('/66login062/', data={ 'username': 'James', 'password': '007' })
            self.assertEqual(current_user.username, 'James')
            response = self.client.get('/admin')
            self.assertEqual(response.status, "200 OK")

class TestNews(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class=Config)
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()

        self.app.config['TESTING'] = True
        self.app.config['LOGIN_DISABLED'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        self.ctx.pop()
        db.session.remove()
        db.drop_all()

    def test_db_news(self):
        u = News(Image = 'test.jpg', Title = 'Title', Description = "Description")
        db.session.add(u)
        db.session.commit()

        posts = News.query.order_by(News.id.desc()).all()

        assert len(posts) == 1
        
        post = posts[0]
        assert post.Title == 'Title' and post.Image == 'test.jpg' and post.Description == "Description"
        
    def test_add_news(self):
        with open(os.path.join(Config.BASE_DIR, 'app/static/test/test.jpg'), 'rb') as img1:
            imgStringIO1 = BytesIO(img1.read())
        response = self.client.post("/addnews/",content_type='multipart/form-data', 
                                        data={'title':'Title',
                                            'description':'Description',
                                            'image': (imgStringIO1, 'test.jpg')}, follow_redirects=True)


        self.assertEqual(response.status, "200 OK")
        posts = News.query.all()

        self.assertEqual(len(posts), 1)
            
        post = posts[0]
        self.assertEqual(post.Title,'Title')
        self.assertEqual(post.Image, 'img/NewsImages/test.jpg')
        self.assertEqual(post.Description, "Description")

    def test_edit_news(self):
        with open(os.path.join(Config.BASE_DIR, 'app/static/test/test.jpg'), 'rb') as img1:
                imgStringIO1 = BytesIO(img1.read())

        self.client.post("/addnews/",content_type='multipart/form-data', 
                                        data={'title':'Title',
                                            'description':'Description',
                                            'image': (imgStringIO1, 'test.jpg')}, follow_redirects=True)

        post = News.query.all()[0]
        self.assertEqual(post.Title,'Title')

        self.client.post("/editnews/",content_type='multipart/form-data', 
                                    data={'newsId':1, 'title':'NewTitle',
                                        'description':'NewDescription'},
                                        follow_redirects=True)

        self.assertEqual(post.Title,'NewTitle')
        self.assertEqual(post.Description,'NewDescription')
        self.assertEqual(post.Image, 'img/NewsImages/test.jpg')
 
    def test_delete_news(self):
        self.client.post("/addnews/",content_type='multipart/form-data', 
                                        data={'title':'Title',
                                            'description':'Description'},
                                            follow_redirects=True)

        posts = News.query.all()
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].id, 1)


        response = self.client.post("/delnews/", data={'newsId': 1},  follow_redirects=True)
        self.assertEqual(response.status, "200 OK")

        posts = News.query.all()
        self.assertEqual(len(posts), 0)

if __name__ == '__main__':
    unittest.main()
