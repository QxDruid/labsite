from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, IntegerField
from wtforms.validators import DataRequired, InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class DeleteImageForm(FlaskForm):
    imageIndex = HiddenField()
    submitDelete = SubmitField('Delete')


class SetImageForm(FlaskForm):
    index = IntegerField('index')
    image = FileField('load image', validators=[FileRequired(), FileAllowed(["jpg", "png"], 'Images only!')])
    submitUpload = SubmitField('Upload')

class AddNewsForm(FlaskForm):
    image = FileField('load image', validators=[FileAllowed(["jpg", "png"], 'Images only!')])
    title = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    fulltext = StringField('full text')
    submitAddNews = SubmitField('Upload')

class DeleteNewsForm(FlaskForm):
    newsId = HiddenField()
    submitDeleteNews = SubmitField('Delete')