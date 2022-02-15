from app.admin import bp
from flask import render_template, url_for, request, redirect, flash
from app import db
from app.db_models import Response, News, User
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import json


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
    unreaded_resp = Response.query.filter(Response.readed==False).order_by(Response.id.desc())
    return render_template("admin_index.html", unreaded_response=unreaded_resp,formReaded=formReaded)


# выход администратора
@bp.route("/admin/response/", methods = ["GET"])
@login_required
def response():
    all_resp = Response.query.order_by(Response.id.desc())
    return render_template("admin_response.html", all_response=all_resp)

# выход администратора
@bp.route("/admin/news/", methods = ["GET"])
@login_required
def news():
    return render_template("admin_news.html")

# выход администратора
@bp.route("/admin/staff/", methods = ["GET"])
@login_required
def staff():
    return redirect(url_for('main.index'))

# выход администратора
@bp.route("/admin/contacts/", methods = ["GET"])
@login_required
def contacts():
    return redirect(url_for('main.index'))

# форма логина для администрации
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

# выход администратора
@bp.route("/logout/", methods = ["GET"])
def logout():
    logout_user()
    return redirect(url_for('main.index'))