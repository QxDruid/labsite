from app.main import bp
from flask import render_template, url_for, request, redirect, flash
from app import db
from app.db_models import Slider_image, News, Person, Research, User
from app.forms import LoginForm, DeleteImageForm, SetImageForm, AddNewsForm, DeleteNewsForm
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename
import os
import config

@bp.route("/", methods = ["POST", "GET"])
@bp.route("/index/", methods = ["POST", "GET"])
def index():
    formDelete = DeleteImageForm()
    formSetImage = SetImageForm()
    formAddNews = AddNewsForm()
    formDeleteNews= DeleteNewsForm()

    if formDelete.submitDelete.data and formDelete.validate_on_submit():
        Slider_image.delete_image(formDelete.imageIndex.data)
        print("delete")
        return redirect(url_for('main.index'))

    if  formSetImage.submitUpload.data  and formSetImage.validate_on_submit():
        f = formSetImage.image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(config.basedir,'app/static/img/SliderImages/{}'.format(filename)))

        Slider_image.set_image(formSetImage.index.data, 'img/SliderImages/{}'.format(filename))

        return redirect(url_for('main.index'))

    if formAddNews.submitAddNews.data and formAddNews.validate_on_submit():
        f = formAddNews.image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(config.basedir, 'app/static/img/NewsImages/{}'.format(filename)))

        News.set_news('img/NewsImages/{}'.format(filename), 
        formAddNews.title.data, 
        formAddNews.description.data, 
        formAddNews.fulltext.data
        )
    
    if formDeleteNews.submitDeleteNews.data and formDeleteNews.validate_on_submit():
        news = News.query.filter_by(id=formDeleteNews.newsId.data).first()
        db.session.delete(news)
        db.session.commit()
        return redirect(url_for('main.index'))



    photos = Slider_image.query.all()
    posts = News.query.order_by(News.id.desc()).all()
    return render_template("index.html", 
        slider_photos=photos,
        posts=posts,
        formDelete=formDelete,
        formSetImage=formSetImage,
        formAddNews=formAddNews,
        formDeleteNews=formDeleteNews,
        lab_description='main_text.html'
    )

@bp.route("/staff/", methods = ["POST", "GET"])
def staff():
    posts = News.query.all()
    staff = Person.query.all()
    return render_template("staff.html",
        posts=posts,
        staff=staff
    )

@bp.route("/research/", methods = ["POST", "GET"])
def research():
    posts = News.query.all()
    researchs = Research.query.all()

    return render_template("research.html",
        posts=posts,
        research=researchs
    )

@bp.route("/login/", methods = ["POST", "GET"])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('main.login'))
        
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template("login.html", form=form)

@bp.route("/logout/", methods = ["GET"])
def logout():
    logout_user()
    return redirect(url_for('main.index'))