from app.main import bp
from flask import render_template, url_for, request, redirect, flash
from app import db
from app.db_models import *
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
import config
import json

# Главная страница
@bp.route("/", methods = ["POST", "GET"])
@bp.route("/index/", methods = ["POST", "GET"])
def index():
    # создаем пагинатор для разбиения новостей на страницы
    page = request.args.get('page')
    if not page:
        page = 1
    else:
        page=int(page)

    posts = News.query.order_by(News.id.desc()).paginate(page, 5, False)

    photos = Slider_image.query.all()
    return render_template("index.html", 
        slider_photos=photos,
        posts=posts,
        lab_description='main_text.html'
    )

# рендер страницы персонала
@bp.route("/staff/", methods = ["POST", "GET"])
def staff():
    formDeleteNews = DeleteNewsForm()
    formPersonAdd = PersonAddForm()
    formDelete = DeleteForm()

    #создаем пагинатор для разбиения новостей на страницы
    page = request.args.get('page')
    if not page:
        page = 1
    else:
        page=int(page)
    posts = News.query.order_by(News.id.desc()).paginate(page, 5, False)
    staff = Person.query.all()
    return render_template("staff.html",
        posts=posts,
        formPersonAdd = formPersonAdd,
        formDeleteNews = formDeleteNews,
        formDelete = formDelete,
        staff=staff
    )


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

    if form.validate_on_submit():

        new_public = Publication()
        new_public.Text = form.text.data
        new_public.Year = form.year.data
        new_public.DOI = form.doi.data
        db.session.add(new_public)
        db.session.commit()
        return redirect(url_for('main.public', active_year=active_year))

    elif formDelete.validate_on_submit():
        public_delete = Publication.query.get(formDelete.Id.data)
        db.session.delete(public_delete)
        db.session.commit()
        return redirect(url_for('main.public', active_year=active_year))

    elif request.method == "POST":
        if not form.year.data:
            flash("Введите Год", "error_year")
        if not form.text.data:
            flash("Введите Ссылку", "error_ref")
        if not form.doi.data:
            flash("Введите DOI", "error_doi")
        return redirect(url_for('main.public', active_year=active_year))

    
        

    for i in range(2030, 2005, -1):
        if Publication.query.filter_by(Year = i).first():
            if active_year == '0':
                active_year = str(i)
            list_.append(str(i))
    form.year.data = active_year

    publics = Publication.query.filter_by(Year = active_year).all()


    return render_template("publications.html", active_year=active_year, years = list_, publics = publics, form=form, formDelete=formDelete)

