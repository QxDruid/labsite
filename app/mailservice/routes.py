from app.mailservice import bp
import uuid
from flask import render_template, url_for, request, redirect, flash
from app import mail
from flask import current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.forms import ResponseForm
from flask_mail import Message
from threading import Thread

uuid_list = []
message_list = {}

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
        #msg.html = f'<h3>Для подтверждения отправки Отзыва в ИЛТССД перейдите по ссылке</h3><p><a href="http://xn--d1ahjyae.xn--p1ai/confirm?uuid={key}">Подтвердить отправку</a></p>'
        try:
            mail.send(msg)
        except:
            pass
    return True

@bp.route("/response/", methods=["POST", "GET"])
def response():
    formResponse = ResponseForm()
    
    if formResponse.validate_on_submit():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        key = str(uuid.uuid4())
        uuid_list.append(key)
        data={'sender_company':formResponse.sender_company.data, 'sender_name':formResponse.sender_name.data,'sender_email':formResponse.sender_email.data,
                                'sender_phone':formResponse.sender_phone.data, 'response':formResponse.response.data, 'sender_function':formResponse.sender_function.data}
        message_list[key]=data

        thread = Thread(target=send_verification_email, args=(current_app._get_current_object(), formResponse.sender_email.data, key))
        thread.setDaemon(True)
        thread.start()
        
        

        flash('Письмо с подтверждением выслано вам на почту', category='confirmation')
        return redirect(url_for('main.index'))

    return render_template('response.html', formResponse=formResponse)

@bp.route("/confirm/", methods=["GET"])
def confirm():
    print(uuid_list)
    print(message_list)
    current_uuid = request.args.get("uuid")
    if current_uuid in uuid_list:

        thread = Thread(target=send_response_email,args=(
                                current_app._get_current_object(),
                                message_list[current_uuid]['sender_company'],  message_list[current_uuid]['sender_name'], message_list[current_uuid]['sender_email'],
                                 message_list[current_uuid]['sender_phone'],  message_list[current_uuid]['response'],  message_list[current_uuid]['sender_function']
                            ))
        thread.setDaemon(True)
        thread.start()

        uuid_list.remove(current_uuid)
        del message_list[current_uuid]
        flash('Отзыв успешно отправлен', category='confirmation_success')
        return redirect(url_for('main.index'))

    flash("Неверный код подтверждения, повторите отправку отзыва", category='confirmation_fail')
    return redirect(url_for('main.index'))