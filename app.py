# Создание нового проекта Flask
import os
from flask import Flask
from flask import render_template
from database import db, Book, Genre
from views import views

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///books.db')
app.register_blueprint(views)
db.init_app(app)

# Добавление данных в базу данных
with app.app_context():
    db.create_all()
    fantasy_genre = Genre.get_or_create(name='Fantasy')
    horror_genre = Genre.get_or_create(name='Horror')
    db.session.add_all([fantasy_genre, horror_genre])
    db.session.commit()


@app.route('/')
def index():
    books = Book.query.order_by(Book.id.desc()).limit(15).all()
    return render_template('index.html', books=books)


@app.route('/genre/<int:genre_id>')
def genre_view(genre_id):
    genre_item = Genre.query.get_or_404(genre_id)
    books = Book.query.filter_by(genre_id=genre_id).all()
    return render_template('genre.html', genre=genre_item, books=books)


if __name__ == '__main__':
    app.run()
