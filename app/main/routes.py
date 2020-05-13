from app.main import bp
from flask import render_template, url_for, request, redirect, flash
from app import db
from app.db_models import Slider_image, News, Person, Research, User
from app.forms import LoginForm
from flask_login import current_user, login_user

class photo(object):
    img = ''
    index = 0


@bp.route("/", methods = ["POST", "GET"])
@bp.route("/index/", methods = ["POST", "GET"])
def index():


    photos = Slider_image.query.all()
    posts = News.query.all()
    return render_template("index.html", 
        slider_photos=photos,
        posts=posts,
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