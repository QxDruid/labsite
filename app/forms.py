from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Вход')

class DeleteImageForm(FlaskForm):
    imageIndex = HiddenField()
    submitDelete = SubmitField('Удалить')


class SetImageForm(FlaskForm):
    index = IntegerField('index')
    image = FileField('load image', validators=[FileRequired(), FileAllowed(["jpg", "png"], 'Images only!')])
    submitUpload = SubmitField('Загрузить')

class AddNewsForm(FlaskForm):
    image = FileField('load image', validators=[FileAllowed(["jpg", "png"], 'Images only!')])
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    fulltext = TextAreaField('full text')
    submitAddNews = SubmitField('Загрузить')

class DeleteNewsForm(FlaskForm):
    newsId = HiddenField()
    submitDeleteNews = SubmitField('Удалить')


class PersonAddForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    secondName = StringField('Фамилия', validators=[DataRequired()])
    middleName = StringField('Отчество', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    info = TextAreaField('О себе', validators=[DataRequired()])
    image = FileField('Загрузить фото', validators=[FileRequired(), FileAllowed(["jpg", "png"], 'Images only!')])
    submitAddPerson = SubmitField('Submit')

class PersonEditForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    secondName = StringField('Фамилия', validators=[DataRequired()])
    middleName = StringField('Отчество', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    info = TextAreaField('О себе', validators=[DataRequired()])
    image = FileField('Загрузить фото', validators=[FileAllowed(["jpg", "png"], 'Images only!')])
    submitAddPerson = SubmitField('Submit')

class DeleteForm(FlaskForm):
    Id = HiddenField()
    submitDelete = SubmitField('Удалить')

class addResearchForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    image = FileField('Загрузить фото', validators=[FileRequired(), FileAllowed(["jpg", "png"], 'Images only!')])
    submit = SubmitField('Загрузить')

class editResearchForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    image = FileField('Загрузить фото', validators=[FileAllowed(["jpg", "png"], 'Images only!')])
    submit = SubmitField('Загрузить')

class PublicationAddForm(FlaskForm):
    id = StringField()
    year = StringField('Год', validators=[DataRequired()])
    text = TextAreaField('Литературная ссылка', validators=[DataRequired()])
    doi = StringField('DOI', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')

class PatentAddForm(FlaskForm):
    id = StringField()
    text = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')

class CommentForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    comment = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')

class SetGalleryImageForm(FlaskForm):
    image = FileField('Изображение', validators=[FileRequired(), FileAllowed(["jpg", "png"], 'Images only!')])
    description = TextAreaField('Описание')
    submitUpload = SubmitField('Загрузить')

class ResponseForm(FlaskForm):
    sender_company = StringField('Организация', validators=[InputRequired('Укажите Организацию')])
    sender_name = StringField('ФИО', validators=[InputRequired('Укажите свои данные')])
    sender_function = StringField('Должность')
    sender_email = StringField('Email', validators=[InputRequired("Введите Email"), Email("Некорекктный Email адрес")])
    sender_phone = StringField('Телефон')
    response = TextAreaField('Отзыв', validators=[InputRequired('Отзыв не может быть пустым')])
    submitUpload = SubmitField('Отправить')