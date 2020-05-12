from app.main import bp
from flask import render_template, url_for

class photo(object):
    img = ''
    index = 0


@bp.route("/")
@bp.route("/index")
def index():
    p = []
    p1 = photo()
    p1.img = url_for('static', filename="img/1.jpg")
    p1.index = 0

    p2 = photo()
    p2.img = url_for('static', filename="img/2.jpg")
    p2.index = 1

    p3 = photo()
    p3.img = url_for('static', filename="img/3.jpg")
    p3.index = 2


    p.append(p1)
    p.append(p2)
    p.append(p3)
    return render_template("index.html", 
    slider_photos=p,
    lab_description='main_text.html'
    )
