from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, InputRequired
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

class DeleteForm(FlaskForm):
    Id = HiddenField()
    submitDelete = SubmitField('Удалить')

class addResearchForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    image = FileField('Загрузить фото', validators=[FileAllowed(["jpg", "png"], 'Images only!')])
    submit = SubmitField('Загрузить')