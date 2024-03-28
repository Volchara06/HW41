from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    books = db.relationship('Book', backref='genre', lazy=True)
# Избегание появления дублей жанров
    @classmethod
    def get_or_create(cls, name):
        genre = cls.query.filter_by(name=name).first()
        if genre is None:
            genre = cls(name=name)
            db.session.add(genre)
            db.session.commit()
        return genre
