from app.mailservice import bp
import uuid
from flask import render_template, url_for, request, redirect, flash
from app import db
from flask import current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.forms import ResponseForm, ConfirmForm
from app.db_models import Response
import secrets
import string
import json

uuid_list = []
message_list = {}

@bp.route("/response/", methods=["POST", "GET"])
def response():
    formResponse = ResponseForm()
    
    if formResponse.validate_on_submit():        
        alphabet = [str(x) for x in range(0,9)]
        key = ''.join(secrets.choice(alphabet) for i in range(5))  # for a 5-character password                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        uuid_list.append(key)
        data={'sender_company':formResponse.sender_company.data, 'sender_name':formResponse.sender_name.data,'sender_email':formResponse.sender_email.data,
                                'sender_phone':formResponse.sender_phone.data, 'response':formResponse.response.data, 'sender_function':formResponse.sender_function.data}
        message_list[key]=data     

        flash(f'Для подтверждения, введите следующий код: {key}', category='confirmation')
        return redirect(url_for('mailservice.confirm', key=key))

    return render_template('response.html', formResponse=formResponse)

@bp.route("/confirm/<key>", methods=["GET", "POST"])
def confirm(key):
    print(uuid_list)
    print(message_list)
    formConfirm = ConfirmForm()
    if formConfirm.validate_on_submit():
        current_uuid = formConfirm.current_uuid.data
        if current_uuid in uuid_list:
            data = message_list[current_uuid]
            response = Response()
            response.fullname = data['sender_name']
            response.organization = data['sender_company']
            response.email = data['sender_email']
            response.position = data['sender_function']
            response.text = data['response']
            response.phone = data['sender_phone']
            response.readed = False
            db.session.add(response)
            db.session.commit()

            del message_list[current_uuid]
            uuid_list.remove(current_uuid)
            flash('Отзыв успешно отправлен', category='confirmation_success')
            return redirect(url_for('main.index'))

        flash(f'Неверный код подтверждения, повторите отправку кода: {key}', category='confirmation_fail')
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