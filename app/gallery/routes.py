from app.gallery import bp
from flask import render_template, url_for, request, redirect, flash
from app import db
from app.db_models import Gallery_image
from app.forms import DeleteForm, SetGalleryImageForm
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
import config
import json

@bp.route("/gallery/", methods=["POST", "GET"])
def gallery():
    formDelete = DeleteForm()
    formAddImage = SetGalleryImageForm()
    
    # Удаление изображений из галереи
    if formDelete.submitDelete.data:
        image_to_delete = Gallery_image.query.get(formDelete.Id.data)
        try:
            os.remove(os.path.join(config.basedir, f'app/static/gallery/{image_to_delete.Image}'))
        except:
            pass

        db.session.delete(image_to_delete)
        db.session.commit()
        return redirect(url_for('gallery.gallery'))

    if formAddImage.submitUpload.data:
        # Добавляем обьект в сессию чтоб получить уникальный ID и использовать его как имя файла
        new_image = Gallery_image()
        db.session.add(new_image)
        db.session.flush()

        # Пишем описание и Имя файла которое используется в шаблонах
        new_image.Description = formAddImage.description.data
        new_image.Image = f'images/gallery/{new_image.id}.jpg'

        # Сохраняем само изображение в папку статик/галерея
        image_file = formAddImage.image.data
        print(image_file)
        image_file.save(os.path.join(config.basedir,f'app/static/images/gallery/{new_image.id}.jpg'))

        # коммитим все в базу и делаем редирект обратно
        db.session.add(new_image)
        db.session.commit()
        return redirect(url_for('gallery.gallery'))

    images = Gallery_image.query.order_by(Gallery_image.id.desc())
    return render_template("gallery.html", image_set=images, formDelete=formDelete, formAddImage=formAddImage)
