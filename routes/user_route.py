
from flask import Blueprint, render_template
from sqlalchemy import desc, func

from database.database import Book, Genre

user_route=Blueprint('user_route',__name__,template_folder='../templates/')

@user_route.route("/")
def index():
  books = Book.query.order_by(desc(Book.id)).limit(15).all()
  return render_template('index.html', books=books)

@user_route.route('/Books')
def get_books():
  books = Book.query.all()
  return render_template('Books.html', books=books,active_page='books')

@user_route.route('/Genres')
def get_genres():
  genres = Genre.query.all()
  return render_template('Genres.html', genres=genres,active_page='genres')
