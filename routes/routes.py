from flask import Flask
from database.database import  db
from routes.api_route import api_route
from routes.user_route import user_route


app=Flask(__name__,static_folder='../static',template_folder='../templates')

app.config.from_object('config.Config')
db.init_app(app)

with app.app_context():
  db.create_all()

app.register_blueprint(user_route)
app.register_blueprint(api_route)