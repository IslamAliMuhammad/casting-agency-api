import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from database.models import setup_db, Movies, Actors
from auth.auth import requires_auth
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
@requires_auth('get:movies')
def get_movies(payload):
  movies = Movies.query.order_by(Movies.id).all()

  movies_formatted = [movie.format() for movie in movies]
  return jsonify({
    'success': True,
    'movies': movies_formatted
  })

@APP.route('/actors')
@requires_auth('get:actors')
def get_actors(payload):
  actors = Actors.query.order_by(Actors.id).all()

  actors_formatted = [actor.format() for actor in actors]
  return jsonify({
    'success': True,
    'actors': actors_formatted
  })
 
@APP.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(payload):

  body = request.get_json()

  if not body:
    abort(400)

  new_title = body.get('title', None)
  new_release_date = body.get('release_date', None)
  
  movie = Movies(title=new_title, release_date=new_release_date)
  movie.insert()

  return jsonify({
    'success': True
  })

@APP.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actors(payload):

  body = request.get_json()

  if not body:
    abort(400)

  new_name = body.get('name', None)
  new_age = body.get('age', None)
  new_gender = body.get('gender', None)

  
  actor = Actors(name=new_name, age=new_age, gender=new_gender)
  actor.insert()

  return jsonify({
    'success': True
  })

@APP.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie_partially(payload, movie_id):
  movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

  body = request.get_json()
  
  title_updated = body.get('title', None)
  release_date_updated = body.get('release_date', None)

  if title_updated:
    movie.title = title_updated
  
  if release_date_updated:
    movie.release_date = release_date_updated

  movie.update()

  return jsonify({
    'success': True
  })

@APP.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def remove_movie(payload, movie_id):
  movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

  movie.delete()

  return jsonify({
    'success': True
  })

@APP.errorhandler(400)
def bad_request(error):
  return jsonify({
    'success': False,
    'error': 400,
    'message': 'bad request'
  }), 400

@APP.errorhandler(500)
def internal_server_error(error):
  return jsonify({
    'success': False,
    'error': 500,
    'message': 'internal server error'
  }), 500

@APP.errorhandler(401)
def unauthorized_error(error):
  return jsonify({
    'success': False,
    'error': 401,
    'message': 'unauthorized error'
  }), 401

@APP.errorhandler(403)
def forbidden(error):
  return jsonify({
    'success': False,
    'error': 403,
    'message': 'forbidden'
  }), 403

@APP.errorhandler(404)
def not_found(error):
  return jsonify({
    'success': False,
    'error': 404,
    'message': 'resource not found'
  }), 404


if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=8080, debug=True)