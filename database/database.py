from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Book(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  title=db.Column(db.String,nullable=False)
  author=db.Column(db.String)
  description=db.Column(db.String)
  img_url=db.Column(db.String)
  
  genre_id=db.Column(db.Integer,db.ForeignKey('genre.id'))
  genre=db.relationship('Genre', backref=db.backref('books', lazy=True))
  
  def __repr__(self):
    return f"Book('{self.title}', '{self.author}')"
  
  def json(self):
    return {'id': self.id, 'title': self.title, 'author': self.author, 'genre': self.genre.name, 'description': self.description}

class Genre(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  name=db.Column(db.String,nullable=False)
  # books=db.relationship('Book',backref='genre')
  
  def __repr__(self):
    return f"Genre:  {self.name}"
  
  def  json(self):
    return {'id':self.id,'name':self.name}
  


  