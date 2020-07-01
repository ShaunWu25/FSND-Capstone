import os, sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, act_movies
from auth import AuthError, requires_auth

DATAS_PER_PAGE = 10

def paginate_pages(request, selection):
  '''
  Paginates and formats database queries
  '''
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * DATAS_PER_PAGE
  end = start + DATAS_PER_PAGE

  datas = [data.format() for data in selection]
  current_datas = datas[start:end]

  return current_datas

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  #----------------------------------------------------------------------------#
  # CORS (API configuration)
  #----------------------------------------------------------------------------#

  CORS(app)
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  @app.route('/')
  def hello():
    return jsonify({'message' : 'Hello World, This is Shaun.' })

  @app.route('/headers')
  @requires_auth()
  def headers(token):
    print(token)
    return 'testing'

  @app.route('/movies')
  def get_movies():
    movies = Movie.query.order_by(Movie.id).all()
    formatted_movies = [movie.format() for movie in movies]
    return jsonify({
      'success' : True,
      'movies': formatted_movies
    })

  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(token):
    actors = Actor.query.order_by(Actor.id).all()
    current_actors = paginate_pages(request, actors)
    if len(current_actors) == 0:
      abort(404)
    return jsonify({
      'success' : True,
      'actors': current_actors,
      'total_actors': len(actors)
      })

  @app.route("/actors/<int:actor_id>")
  def get_specific_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)
    else:
      return jsonify({
      'success' : True,
      'actors': actor.format()
      })

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  def update_actor(actor_id):
    body = request.get_json()
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      if actor is None:
        abort(404)
      if 'age' in body:
        actor.age = int(body.get('age'))

      actor.update()
      return jsonify({
        'success': True,
        'id': actor.id
      })

    except:
      abort(400)

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  def delete_actor(actor_id):
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      if actor is None:
        abort(404)
    
      actor.delete()
      actors = Actor.query.order_by(Actor.id).all()
      current_actors = paginate_pages(request, actors)

      return jsonify({
          'success' : True,
          'deleted': actor.id,
          'actors': current_actors,
          'total_actors': len(actors)
        })

    except:
      abort(422)

  @app.route('/actors', methods=['POST'])
  def create_actor():
    body = request.get_json()

    new_name = body.get('name')
    new_gender = body.get('gender')
    new_age = body.get('age')

    try:
      actor = Actor(name = new_name, gender = new_gender, age = new_age)
      actor.insert()

      actors = Actor.query.order_by(Actor.id).all()
      current_actors = paginate_pages(request, actors)

      return jsonify({
        'success' : True,
        'created': actor.id,
        'actors': current_actors,
        'total_actors': len(actors)
      })

    except:
      abort(422)

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405
  
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
