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
def index():
    formReaded= DeleteForm()
    if formReaded.submitDelete.data and formReaded.validate_on_submit():
        response = Response.query.filter_by(id=formReaded.Id.data).first()
        response.readed = True
        db.session.add(response)
        db.session.commit()
    all_resp = Response.query.order_by(Response.id.desc())
    unreaded_resp = [resp for resp in all_resp if resp.readed == False]
    print(unreaded_resp)
    return render_template("admin_index.html", unreaded_response=unreaded_resp, all_resp = all_resp, formReaded=formReaded)

# выход администратора
@login_required
@bp.route("/admin/news/", methods = ["GET"])
def news():
    return render_template("admin_news.html")

# выход администратора
@login_required
@bp.route("/admin/staff/", methods = ["GET"])
def staff():
    return redirect(url_for('main.index'))

# выход администратора
@login_required
@bp.route("/admin/contacts/", methods = ["GET"])
def contacts():
    return redirect(url_for('main.index'))

# выход администратора
@login_required
@bp.route("/admin/response/", methods = ["GET"])
def response():
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