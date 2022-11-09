from ast import Try
from crypt import methods
from app.admin import bp
from flask import render_template, url_for, request, redirect, flash, send_from_directory
from app import db
from app.db_models import Response, News, User, Slider_image
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from .random_gen import create_table, testtable
import os
import config

# Главная страница админа
@bp.route("/admin", methods = ["POST", "GET"])
@bp.route("/admin/index/", methods = ["POST", "GET"])
@login_required
def index():
    formReaded = DeleteForm()
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

# Обработчик просмотра всех отзывов
@bp.route("/admin/random/", methods = ["POST", "GET"])
@login_required
def random():
    choices=(0, "BB", "Metal", "Introskope")
    #directory = os.path.join(config.basedir, 'app/tmp')
    form = getRandomForm()
    if form.submit.data:
        tssd_type = form.type.data
        filename = f"{choices[int(tssd_type)]}_{form.name.data}"
        create_table(f'/app/tmp/{filename}', int(tssd_type))
        return send_from_directory("/app/tmp/", f"{filename}.xls", as_attachment=True)
        
    return render_template("admin_random.html", form=form)

    

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
            f.save(os.path.join(config.basedir, 'app/static/images/news/{}'.format(filename)))
        else:
            filename = None

        News.set_news('images/news/{}'.format(filename), 
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
            f.save(os.path.join(config.basedir, 'app/static/images/news/{}'.format(filename)))
            post.Image = 'images/news/{}'.format(filename)

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
    if formDeleteNews.newsId.data and formDeleteNews.validate_on_submit():
        news = News.query.filter_by(id=formDeleteNews.newsId.data).first()
        db.session.delete(news)
        db.session.commit()
        try:
            os.remove(os.path.join(config.basedir, 'app/static/{}'.format(news.Image)))
        except:
            pass
    return redirect(url_for('admin.news'))

@bp.route('/admin/carousel')
@login_required
def carousel():
    slider = Slider_image.query.order_by(Slider_image.Index)
    formAddImage = SetImageForm()
    formDelete=DeleteForm()
    return render_template("admin_carousel.html", slider=slider, formAddImage=formAddImage, formDelete=formDelete)



# добавление картинки в карусель
@bp.route('/admin/carousel/add', methods=["POST"])
@login_required
def addcarouselimage():
    formSetImage=SetImageForm()

    if formSetImage.submitUpload.data:# and formSetImage.validate_on_submit():
        images = Slider_image.query.all()
        index = int(formSetImage.index.data)
        for img in images:
            if img.Index >= index:
                img.Index = img.Index + 1
                db.session.add(img)
        db.session.commit()

        f = formSetImage.image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(config.basedir,f'app/static/images/slider/{filename}{index}'))
        Slider_image.set_image(index, f'images/slider/{filename}{index}')
    
    return redirect(url_for('admin.carousel'))

# удаление картинки из карусели
@bp.route('/admin/carousel/del', methods=["POST"])
@login_required
def delcarouselimage():
    formDelete=DeleteForm()

    if formDelete.submitDelete.data:
        index = int(formDelete.Id.data)
        img = Slider_image.query.filter_by(Index=index).first()
        Slider_image.delete_image(index)
        try:
            os.remove(os.path.join(config.basedir,'app/static/{}'.format(img.Image)))
        except:
            pass

        images = Slider_image.query.all()

        for img in images:
            if img.Index > index:
                img.Index = img.Index - 1
                db.session.add(img)
        db.session.commit()

    return redirect(url_for('admin.carousel'))

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