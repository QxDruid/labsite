from app.main import bp
from flask import render_template, url_for, request, redirect, flash
from app import db
from app.db_models import Slider_image, News, Person, Research, User, Publication
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
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
@bp.route('/research/', methods = ["POST", "GET"])
def research():
    formAddResearch = addResearchForm()
    formDeleteResearch = DeleteForm()
    formDeleteNews = DeleteNewsForm()

    researches = Research.query.order_by(Research.Title).all()
    posts = News.query.order_by(News.id.desc()).all()
    return render_template('research.html',
        researches=researches,
        posts=posts,
        formDeleteResearch=formDeleteResearch,
        formDeleteNews=formDeleteNews,
        formAddResearch = formAddResearch
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
@login_required
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
    return redirect(url_for('main.index'))

# обработка добавления новостей
@bp.route('/addnews/', methods=["POST"])
@login_required
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
@login_required
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
    else:
        if not form.name.data:
            flash("Введите имя",'error_name')
        if not form.secondName.data:
            flash("Введите фамилию",'error_secondname')
        if not form.middleName.data:
            flash("Введите отчество",'error_middlename')
        if not form.image.data:
            flash("Выберите изображение",'error_image')
        if not form.position.data:
            flash("Введите должность",'error_position')
        if not form.info.data:
            flash("Введите описание",'error_info')

    return redirect(url_for('main.staff'))

@bp.route('/delperson/', methods=["POST"])
@login_required
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

@bp.route('/addresearch/', methods=["POST"])
@login_required
def addresearch():
    form = addResearchForm()
    if form.validate_on_submit():
        research = Research()
        research.Title = form.title.data
        research.Description = form.description.data
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(config.basedir, "app/static/img/ResearchImages/{}".format(filename)))
        research.Image = "img/ResearchImages/{}".format(filename)
        db.session.add(research)
        db.session.commit()
    else:
        if not form.title.data:
            flash("Введите заголовок",'error_title')
        if not form.image.data:
            flash("Выберите изображение",'error_image')
        if not form.description.data:
            flash("Введите описание",'error_description')

    return redirect(url_for("main.research"))

@bp.route("/delresearch/", methods=["POST"])
@login_required
def delresearch():
    form = DeleteForm()
    if form.validate_on_submit():
        research = Research.query.get(form.Id.data)
        try:
            os.remove(os.path.join(config.basedir, "app/static/{}".format(research.Image)))
        except:
            pass # сделать флеш что нет такой картинки, и было все удалено

        db.session.delete(research)
        db.session.commit()
    return redirect(url_for("main.research"))

@bp.route("/editresearch/<researchId>", methods=["POST", "GET"])
@login_required
def editresearch(researchId):
    formEditResearch = editResearchForm()
    research = Research.query.get(researchId)

    # Если все поля формы валидны
    if formEditResearch.validate_on_submit():
        if formEditResearch.image.data:
            f = formEditResearch.image.data
            filename = secure_filename(f.filename)
            try:
                os.remove(os.path.join(config.basedir, "app/static/{}".format(research.Image)))
            except:
                pass
            f.save(os.path.join(config.basedir,"app/static/img/ResearchImages/{}".format(filename)))
            research.Image = "img/ResearchImages/{}".format(filename)
        
        
        research.Description = formEditResearch.description.data
        research.Title = formEditResearch.title.data
        db.session.add(research)
        db.session.commit()
        return redirect(url_for('main.editresearch', researchId=researchId))

    # если была отправка формы но поля не валидны (иначе мы бы уже ушли в редирект выше)
    if request.method == "POST":
        if not formEditResearch.title.data:
            flash("Заголовок не может быть пустым", "error_title")
        if not formEditResearch.description.data:
            flash("Описание не может быть пустым", "error_description")
        return redirect(url_for('main.editresearch', researchId=researchId))

    # если только пришли на страницу через гет
    formEditResearch.title.data = research.Title
    formEditResearch.description.data = research.Description
    return render_template('editresearch.html',
        research=research,
        formEditResearch=formEditResearch
    )


@bp.route("/editperson/<personId>", methods=["POST","GET"])
@login_required
def editperson(personId):
    formEditPerson = PersonEditForm()
    person = Person.query.get(personId)

    if formEditPerson.validate_on_submit():
        if formEditPerson.image.data:
            f = formEditPerson.image.data
            filename = secure_filename(f.filename)
            try:
                os.remove(os.path.join(config.basedir, "app/static/{}".format(person.Image)))
            except:
                pass
            f.save(os.path.join(config.basedir, "app/static/img/PersonImage/{}".format(filename)))
            person.Image = "img/PersonImage/{}".format(filename)
        
        person.FirstName = formEditPerson.name.data
        person.SecondName = formEditPerson.secondName.data
        person.MiddleName = formEditPerson.middleName.data
        person.Info = formEditPerson.info.data
        person.Position = formEditPerson.position.data
        db.session.add(person)
        db.session.commit()
        return redirect(url_for("main.editperson", personId = personId))

    elif request.method == "POST":
        if not formEditPerson.name.data:
            flash("Введите Имя", "error_name")
        if not formEditPerson.secondName.data:
            flash("Введите Фамилию", "error_secondname")
        if not formEditPerson.middleName.data:
            flash("Введите Отчество", "error_middlename")
        if not formEditPerson.info.data:
            flash("Введите описание", "error_info")
        if not formEditPerson.position.data:
            flash("Введите должность", "error_position")
        
        return redirect(url_for('main.editperson', personId = personId))

    formEditPerson.name.data = person.FirstName
    formEditPerson.middleName.data  = person.MiddleName
    formEditPerson.secondName.data  = person.SecondName
    formEditPerson.position.data  = person.Position
    formEditPerson.info.data  = person.Info

    return render_template("editperson.html",
        person=person,
        formEditPerson=formEditPerson
    )

@bp.route("/contacts/")
def contacts():
    return render_template("contacts.html")

@bp.route("/public/<active_year>", methods=["POST", "GET"])
def public(active_year):
    form = PublicationAddForm()
    formDelete = DeleteForm()
    list_ = []
    print("qqqqqq")

    if form.validate_on_submit():
        print("asdasdasdasd")
        new_public = Publication()
        new_public.Text = form.text.data
        new_public.Year = form.year.data
        new_public.DOI = form.doi.data
        db.session.add(new_public)
        db.session.commit()
        return redirect(url_for('main.public', active_year=active_year))

    if formDelete.validate_on_submit():
        public_delete = Publication.query.get(formDelete.Id.data)
        db.session.delete(public_delete)
        db.session.commit()
        return redirect(url_for('main.public', active_year=active_year))


    for i in range(2030, 2005, -1):
        if Publication.query.filter_by(Year = i).first():
            if active_year == '0':
                active_year = str(i)
            list_.append(str(i))
    form.year.data = active_year

    publics = Publication.query.filter_by(Year = active_year).all()


    return render_template("publications.html", active_year=active_year, years = list_, publics = publics, form=form, formDelete=formDelete)