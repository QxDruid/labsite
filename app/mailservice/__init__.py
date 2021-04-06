from flask import Blueprint

bp = Blueprint('mailservice', __name__)

from app.mailservice import routes