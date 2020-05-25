from app import create_app, db
from app.db_models import User, Slider_image, News, Person, Research

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Slider_image':Slider_image, 'News':News, 'Person':Person, 'Research':Research, 'app': app}

if __name__ == "__main__":
    app.run()