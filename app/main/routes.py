from app.main import bp
from flask import render_template, url_for, request, redirect, flash
from app import db
from app.db_models import Slider_image, News, Person, Research, User
from app.forms import LoginForm, DeleteImageForm, SetImageForm, AddNewsForm, DeleteNewsForm, PersonAddForm, DeleteForm
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename
import os
import config

# Главная страница
@bp.route("/", methods = ["POST", "GET"])
@bp.route("/index/", methods = ["POST", "GET"])
def index():
    formDelete = DeleteImageForm() #Форма удаления картинки из слайдера
    formSetImage = SetImageForm() #Добавление катринки в слайдер
    formAddNews = AddNewsForm() # добавить новость(нужна тут для отрисовки) обработка функции в main.addnews
    formDeleteNews= DeleteNewsForm() # удалить новость(нужна тут для отрисовки) обработка функции в main.delnews
    
    # удаление картинки из карусели
    if formDelete.submitDelete.data and formDelete.validate_on_submit():
        img = Slider_image.query.filter_by(Index=formDelete.imageIndex.data).first()
        Slider_image.delete_image(formDelete.imageIndex.data)
        os.remove(os.path.join(config.basedir,'app/static/{}'.format(img.Image)))
        return redirect(url_for('main.index'))

    # добавление картинки в карусель
    if  formSetImage.submitUpload.data  and formSetImage.validate_on_submit():
        f = formSetImage.image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(config.basedir,'app/static/img/SliderImages/{}'.format(filename)))

        Slider_image.set_image(formSetImage.index.data, 'img/SliderImages/{}'.format(filename))

        return redirect(url_for('main.index'))

    # рендер страницы если запрос "GET"
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

# рендер страницы персонала
@bp.route("/staff/", methods = ["POST", "GET"])
def staff():
    formDeleteNews = DeleteNewsForm()
    formPersonAdd = PersonAddForm()
    formDelete = DeleteForm()
    posts = News.query.order_by(News.id.desc()).all()
    staff = Person.query.all()
    return render_template("staff.html",
        posts=posts,
        formPersonAdd = formPersonAdd,
        formDeleteNews = formDeleteNews,
        formDelete = formDelete,
        staff=staff
    )

# рендер страницы исследования
@bp.route('/research/')
def research():
    researches = Research.query.all()
    posts = News.query.order_by(News.id.desc()).all()
    formDeleteNews = DeleteNewsForm()
    return render_template('research.html',
        researches=researches,
        posts=posts,
        formDeleteNews=formDeleteNews
    )
# форма логина для администрации
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

# выход администратора
@bp.route("/logout/", methods = ["GET"])
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# редактор новости
@bp.route("/editnews/<newsId>",methods=["POST", "GET"])
def editnews(newsId):
    form = AddNewsForm()
    post = News.query.get(newsId)
    if form.validate_on_submit(): 
        if form.image.data:
            try:
                os.remove(os.path.join(config.basedir, 'app/static/{}'.format(post.Image)))
            except:
                pass
            f = form.image.data
            filename=secure_filename(f.filename)
            f.save(os.path.join(config.basedir, 'app/static/img/NewsImages/{}'.format(filename)))
            post.Image = 'img/NewsImages/{}'.format(filename)

        post.Title = form.title.data
        post.Description = form.description.data
        post.Fulltext = form.fulltext.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.editnews', newsId=post.id))


    
    form.title.data = post.Title
    form.description.data = post.Description
    form.fulltext.data = post.Fulltext

    return render_template("editnews.html", post=post, form=form)

# обработка удаления новостей
@bp.route('/delnews/', methods=["POST"])
def delnews():
    formDeleteNews= DeleteNewsForm()
    if formDeleteNews.submitDeleteNews.data and formDeleteNews.validate_on_submit():
        news = News.query.filter_by(id=formDeleteNews.newsId.data).first()
        db.session.delete(news)
        db.session.commit()
        try:
            os.remove(os.path.join(config.basedir, 'app/static/{}'.format(news.Image)))
        except:
            pass
    return redirect(url_for('main.index'))

# обработка добавления новостей
@bp.route('/addnews/', methods=["POST"])
def addnews():

    formAddNews = AddNewsForm()
    if formAddNews.validate_on_submit():
        f = formAddNews.image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(config.basedir, 'app/static/img/NewsImages/{}'.format(filename)))

        News.set_news('img/NewsImages/{}'.format(filename), 
            formAddNews.title.data, 
            formAddNews.description.data, 
            formAddNews.fulltext.data
        )

    return redirect(url_for("main.index"))

@bp.route('/addPerson/', methods=["POST"])
def addPerson():
    form = PersonAddForm()
    if form.validate_on_submit():
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(config.basedir, 'app/static/img/StaffImages/{}'.format(filename)))

        Person.set_person(form.name.data, 
            form.secondName.data, 
            form.middleName.data, 
            form.position.data, 
            form.info.data, 
            'img/StaffImages/{}'.format(filename)
            )

    return redirect(url_for('main.staff'))

@bp.route('/delperson/', methods=["POST"])
def delperson():
    formDelete = DeleteForm()
    if formDelete.validate_on_submit():
        pers = Person.query.get(formDelete.Id.data)
        try:
            os.remove(os.path.join(config.basedir, "app/static/{}".format(pers.Image)))
        except:
            pass

        Person.del_person(pers)
        
    return redirect(url_for('main.staff'))

