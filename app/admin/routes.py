from app.admin import bp
from flask import render_template, url_for, request, redirect, flash
from app import db
from app.db_models import Response, News, User, Slider_image
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
import config

# Главная страница админа
@bp.route("/admin", methods = ["POST", "GET"])
@bp.route("/admin/index/", methods = ["POST", "GET"])
@login_required
def index():
    formReaded= DeleteForm()
    if formReaded.submitDelete.data and formReaded.validate_on_submit():
        response = Response.query.filter_by(id=formReaded.Id.data).first()
        response.readed = True
        db.session.add(response)
        db.session.commit()
    unreaded_resp = Response.query.filter(Response.readed==False, Response.verified==True).order_by(Response.id.desc())
    return render_template("admin_index.html", unreaded_response=unreaded_resp,formReaded=formReaded)


# Обработчик просмотра всех отзывов
@bp.route("/admin/response/", methods = ["GET"])
@login_required
def response():
    all_resp = Response.query.filter(Response.verified==True).order_by(Response.id.desc())
    return render_template("admin_response.html", all_response=all_resp)

# Страница управления новостями
@bp.route("/admin/news/", methods = ["GET", "POST"])
@login_required
def news():
    formDeleteNews= DeleteNewsForm()
    form = AddNewsForm()
    formAddNews = AddNewsForm()
    page = request.args.get('page')
    if not page:
        page = 1
    else:
        page=int(page)
    
    posts = News.query.order_by(News.id.desc()).paginate(page, 5, False)
    return render_template("admin_news.html", posts=posts, form=form, formDeleteNews=formDeleteNews, formAddNews=formAddNews)



# Обработчик добавления новости
@bp.route("/addnews/",methods=["POST"])
@login_required
def addnews():
    formAddNews = AddNewsForm()
    if formAddNews.validate_on_submit():
        if formAddNews.image.data:
            f = formAddNews.image.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(config.basedir, 'app/static/img/NewsImages/{}'.format(filename)))
        else:
            filename = None

        News.set_news('img/NewsImages/{}'.format(filename), 
            formAddNews.title.data, 
            formAddNews.description.data, 
            formAddNews.fulltext.data
        )
    return redirect(url_for("admin.news"))

# Обработчик редактирования новости
@bp.route("/editnews/",methods=["POST"])
@login_required
def editnews():
    form = AddNewsForm()
    if form.validate_on_submit() and form.newsId.data:
        post = News.query.get(form.newsId.data)
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
    return redirect(url_for('admin.news'))


# Обработчик удаления новостей
@bp.route('/delnews/', methods=["POST"])
@login_required
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
    return redirect(url_for('admin.news'))

@bp.route('/carousel/add')
def addcarouselimage():
    formSetImage=formSetImage()
    formDelete=formDelete()
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

# Страница редактирования персонала
@bp.route("/admin/staff/", methods = ["GET"])
@login_required
def staff():
    return redirect(url_for('main.index'))

# Страница редактирования контактов
@bp.route("/admin/contacts/", methods = ["GET"])
@login_required
def contacts():
    return redirect(url_for('main.index'))

# Форма логина для администрации
@bp.route("/66login062/", methods = ["POST", "GET"])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('admin.login'))
        
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('admin.index'))
    return render_template("login.html", form=form)

# Выход администратора
@bp.route("/logout/", methods = ["GET"])
def logout():
    logout_user()
    return redirect(url_for('main.index'))