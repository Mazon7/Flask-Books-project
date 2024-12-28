from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, asc
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    added = db.Column(db.DateTime, nullable=False, default=func.now())

    genre_id = db.Column(db.Integer, db.ForeignKey(
        "genre.id", ondelete='SET NULL'))
    genre = relationship("Genre", back_populates="books")

    def __repr__(self):
        return f"Book(name={self.name!r})"


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    books = relationship("Book", back_populates="genre")
    added = db.Column(db.DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f"Genre(name={self.name!r})"
