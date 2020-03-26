import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from database.models import setup_db, Movies, Actors

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  return app

APP = create_app()
setup_db(APP)


@APP.route('/')
def index():
  return 'hello world'

@APP.route('/movies')
def get_movies():
  movies = Movies.query.order_by(Movies.id).all()

  movies_formatted = [movie.format() for movie in movies]
  return jsonify({
    'success': True,
    'movies': movies_formatted
  })

@APP.route('/actors')
def get_actors():
  actors = Actors.query.order_by(Actors.id).all()

  actors_formatted = [actor.format() for actor in actors]
  return jsonify({
    'success': True,
    'actors': actors_formatted
  })
 
@APP.route('/movies', methods=['POST'])
def create_movie():

  body = request.get_json()
  new_title = body.get('title', None)
  new_release_date = body.get('release_date', None)
  
  movie = Movies(title=new_title, release_date=new_release_date)
  movie.insert()

  return jsonify({
    'success': True
  })



if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=8080, debug=True)