

import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import desc, func
from werkzeug.utils import secure_filename
from config  import Config

from database.database import Book, Genre,db

UPLOAD_FOLDER=Config.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def check_filename(filename):
  print(filename)
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_file(filename):
  return secure_filename(filename)

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
    file_path=''
    if 'image' in request.files:
      print(f"got image")
      file = request.files['image']
      if file and check_filename(file.filename):
        print(f"Uploading file: {file.filename}")
        file_path = os.path.join(UPLOAD_FOLDER, secure_file(file.filename))
        print(f"Attempting to save file to: {file_path}")
        try:
          file.save(file_path)
          print(f"File saved to: {file_path}")
        except Exception as e:
          flash(f'An error occurred while saving the file: {str(e)}', 'danger')
          return redirect(request.url)
      else:
          flash('Invalid file', 'danger')
          return redirect(request.url)

    title = request.form.get('title')
    author = request.form.get('author')
    description=request.form.get('description')
    genre_id = request.form.get('genre')
    new_book=Book(
      title=title,
      author=author,
      description=description,
      genre_id=genre_id,
      img_url=file_path
      )

    db.session.add(new_book)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      flash('An error occurred while saving to the database.', 'danger')
      return redirect(request.url)
    
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
    
