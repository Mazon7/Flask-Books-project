#!/usr/bin/env python

import os
import requests

from flask import Flask
from flask import render_template

from database import db, Genre, Book, desc


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# os.getenv("SQLALCHEMY_DATABASE_URI")
db.init_app(app)


def get_genre(genre, lst,  default="Genre not found"):
    lst_lower = [x.lower() for x in lst]
    return genre if genre.lower() in lst_lower else default


def fetch_books_from_api():
    url = f"https://www.freetestapi.com/api/v1/books"
    response = requests.get(url)
    if response.status_code == 200:
        books = response.json()
        for item in books:
            title = item.get("title", "Unknown Title")
            genres = item.get("genre", "Unknown Genre")
            genre_name = genres[0] if genres else "Unknown Genre"

            # Search genre in DB
            search_genre = Genre.query.filter_by(name=genre_name).first()

            # Add new genre if it does not exist
            if search_genre is None:
                # Create Genre object
                genre_obj = Genre(name=genre_name)
                # db.session.add(genre_obj)

                # Create Book object with new Genre
                book = Book(name=title, genre=genre_obj)

            else:
                print(f"The genre {genre_name} already exists!")

                # Create Book object with existed Genre
                book = Book(name=title, genre=search_genre)

            # Save Genres and Books into the DB
            db.session.add(genre_obj)
            db.session.add(book)
        print(f"Added {len(books)} books to the database.")
    else:
        print(f"Failed to fetch books. Status code: {response.status_code}")


with app.app_context():
    # Clean DB
    # Create all data in DB
    db.drop_all()
    db.create_all()

    # # # HARCODED GENRES # # #
    # genres = ['Fantasy', 'Science fiction', 'Horror', 'Mystery', 'Historical Fiction', 'Romance', 'Adventure fiction', 'Literary fiction', 'Young adult', 'Fiction', 'Fairy tale',
    #           'Graphic novel', 'Suspense', 'Thriller', 'Classic', 'Dystopian', 'History', 'Literary realism', 'Magical Realism', 'Short story', 'Western fiction', "Women's fiction", 'Autobiographies']
    # for genre in genres:
    #     db.session.add(Genre(name=genre))

    fetch_books_from_api()

    db.session.commit()


@ app.route("/")
def all_books():
    books = Book.query.order_by(Book.added, desc(Book.id)).limit(15).all()
    return render_template("layout.html", books=books)


@ app.route("/genres/<int:genre_id>")
def books_by_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return render_template("books_by_genre.html", genre_name=genre.name, books=genre.books)


if __name__ == '__main__':
    app.run()
