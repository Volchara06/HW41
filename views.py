from flask import Blueprint, render_template, request, redirect, url_for
from database import db, Book, Genre

# Создание экземпляра Blueprint для организации представлений
views = Blueprint('views', __name__)


@views.route('/')
def index():
    books = Book.query.order_by(Book.id.desc()).limit(15).all()
    return render_template('index.html', books=books)


@views.route('/genre/<int:genre_id>')
def genre_view(genre_id):
    genre_item = Genre.query.get_or_404(genre_id)
    books = Book.query.filter_by(genre_id=genre_id).all()
    return render_template('genre.html', genre=genre_item, books=books)


@views.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre_id = request.form['genre_id']

        new_book = Book(title=title, author=author, genre_id=genre_id)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('views.index'))

    genres = Genre.query.all()
    return render_template('add_book.html', genres=genres)
