
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
  genres = db.session.query(
    Genre.id,
    Genre.name,
    func.count(Book.id).label('book_count') 
).outerjoin(Book).group_by(Genre.id, Genre.name).all()
  return render_template('Genres.html', genres=genres,active_page='genres')

@user_route.route('/Books/create',methods=['GET','POST'])
def create_book():
  if request.method == 'POST':
    print("Form submitted!")  # Debugging line
    print(request.form)  # Print the entire form data
    title = request.form.get('title')
    author = request.form.get('author')
    description=request.form.get('description')
    genre_id = request.form.get('genre')
    new_book=Book(
      title=title,
      author=author,
      description=description,
      genre_id=genre_id
      )
    print(title,author,description,genre_id)
    db.session.add(new_book)
    db.session.commit()
    
    flash('New book created!','success')
    return  redirect(url_for('user_route.get_books'))
  genres=Genre.query.all()
  return  render_template('Books.html',genres=genres,active_page='books',flag='create')

@user_route.route('/Genres/create',methods=['GET','POST'])
def create_genre():
  if request.method == 'POST':
    name = request.form.get('name')
    description=request.form.get('description')
    new_book=Genre(
      name=name,
      description=description
      )
    db.session.add(new_book)
    db.session.commit()
    
    flash('New genre created!','success')
    return  redirect(url_for('user_route.get_genres'))
  genres=Genre.query.all()
  return  render_template('Genres.html',active_page='genres',flag='create')
    
