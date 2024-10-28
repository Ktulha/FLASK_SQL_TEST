
from flask import Blueprint, render_template
from sqlalchemy import desc, func

from database.database import Book

user_route=Blueprint('user_route',__name__,template_folder='../templates/')

@user_route.route("/")
def index():
  books = Book.query.order_by(desc(Book.id)).limit(15).all()
  return render_template('index.html', books=books)

