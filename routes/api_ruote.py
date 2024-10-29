from flask import Blueprint, jsonify, request

from database.database import Book, db


api_route=Blueprint('api_route',__name__,url_prefix="/api/v1" )

@api_route.route('/books/<int:id>',methods=['GET','PUT','DELETE'])

def book_rud(id: int):
    book = Book.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(book.json()) 
    elif request.method == 'PUT':
        data = request.json
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.published_date = data.get('published_date', book.published_date)
        db.session.commit()
        return jsonify(book.json()), 200
    elif request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'}), 204

@api_route.route('/create_book', methods=['POST'])
def create_book():
    data = request.json
    new_book = Book(
        title=data['title'],
        author=data['author'],
        description=data['description']
        genre_id=data['genre_id']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201
  