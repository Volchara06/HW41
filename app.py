import os
# Создание нового проекта Flask
from flask import Flask
from flask import render_template
from database import db, Book, Genre

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///books.db')
db.init_app(app)

with app.app_context():
    # Добавление данных в базу данных
    db.create_all()

    # Примеры книг для тестирования
    fantasy_genre = Genre(name='Fantasy')
    horror_genre = Genre(name='Horror')

    book1 = Book(title='Book 1', author='Author 1', genre=fantasy_genre)
    book2 = Book(title='Book 2', author='Author 2', genre=fantasy_genre)
    book3 = Book(title='Book 3', author='Author 3', genre=horror_genre)

    db.session.add_all([fantasy_genre, horror_genre, book1, book2, book3])
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
