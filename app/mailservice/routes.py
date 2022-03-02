from app.mailservice import bp
import uuid
from flask import render_template, url_for, request, redirect, flash, make_response
from app import db
from flask import current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.forms import ResponseForm, ConfirmForm
from app.db_models import Response
import secrets
import string
import json


# get response and generate password to confirm
@bp.route("/response/", methods=["POST", "GET"])
def response():
    formResponse = ResponseForm()
    
    if formResponse.validate_on_submit():        
        alphabet = '123456789'
        key = ''.join(secrets.choice(alphabet) for i in range(5))  # for a 5-character password
   
        response = Response()
        response.fullname = formResponse.sender_name.data
        response.organization = formResponse.sender_company.data
        response.email = formResponse.sender_email.data
        response.position = formResponse.sender_function.data
        response.text = formResponse.response.data
        response.phone = formResponse.sender_phone.data
        response.readed = False
        response.verified = False

        db.session.add(response)
        db.session.commit()

        flash(f'Для подтверждения, скопируйте и отправьте код: {key}', category='confirmation')
        resp = make_response(redirect(url_for('mailservice.confirm', key=key)))
        resp.set_cookie('key', key)
        resp.set_cookie('resp_id', str(response.id))
  
        return resp

    return render_template('response.html', formResponse=formResponse)

@bp.route("/confirm/<key>", methods=["GET", "POST"])
def confirm(key):
    formConfirm = ConfirmForm()
    if formConfirm.validate_on_submit():
        current_uuid = formConfirm.current_uuid.data
        uuid = request.cookies.get('key')
        resp_id = int(request.cookies.get('resp_id'))

        if current_uuid == uuid:
            response = Response.query.filter_by(id=resp_id).first()
            response.verified = True
            db.session.add(response)
            db.session.commit()

            flash('Отзыв успешно отправлен', category='confirmation_success')
            resp = make_response(redirect(url_for('main.index')))
            resp.delete_cookie('key')
            return resp

        flash(f'Неверный код подтверждения, скопируйте и отправьте код: {key}', category='confirmation_fail')
        return redirect(url_for('mailservice.confirm',key=key))

    return render_template('response_confirm.html', formConfirm=formConfirm, key=key)




    '''
def send_response_email(app, company, sender, sender_email, sender_phone, response, sender_function):
    with app.app_context():
        msg = Message(subject=f'Отзыв с Сайта ИЛТТСД от: {company}', sender=app.config['MAIL_USERNAME'], recipients=[app.config['MAIL_DESTINATION']])
        msg.body = f'Организация: {company}\nОтправитель: {sender_function} {sender}.\nemail: {sender_email}\nТелефон: {sender_phone}\n\nОтзыв:\n{response}'
        msg.html = render_template('response_message.html',company=company, sender=sender, sender_email=sender_email,
                                sender_phone=sender_phone, response=response, sender_function=sender_function)
        try:
            mail.send(msg)
        except:
            pass
    return True

def send_verification_email(app, destination, key):
    with app.app_context():
        msg = Message(subject=f'Поддверждение отправки отзыва ИЛТССД', sender=app.config['MAIL_USERNAME'], recipients=[destination])
        msg.body = f'Для подтверждения отправки Отзыва в ИЛТССД перейдите по ссылке http://xn--d1ahjyae.xn--p1ai/confirm?uuid={key}'
        msg.html = f'<h3>Для подтверждения отправки Отзыва в ИЛТССД перейдите по ссылке</h3><p>http://xn--d1ahjyae.xn--p1ai/confirm?uuid={key}</p>'
        try:
            mail.send(msg)
        except:
            pass
    return True
'''