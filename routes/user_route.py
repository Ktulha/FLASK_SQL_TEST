
from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import desc, func

from database.database import Book, Genre,db

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

@user_route.route('/Books/create',methods=['GET','POST'])
def create_book():
  if request.method == 'POST':
    title = request.form.get('title')
    author = request.form.get('author')
    description=request.form.get('description')
    genre_id = request.form.get('genre_id')
    new_book=Book(
      title=title,
      author=author,
      description=description,
      genre_id=genre_id
      )
    db.session.add(new_book)
    db.session.commit()
    
    flash('New book created!','success')
    return  redirect(url_for('user_route.get_books'))
  genres=Genre.query.all()
  return  render_template('Books.html',genres=genres,active_page='books',flag='create')


    
