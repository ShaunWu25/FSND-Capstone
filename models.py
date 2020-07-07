import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Float
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_migrate import Migrate
import sys

'''
database_path = os.environ.get('DATABASE_URL')

if not database_path:
  database_path = 'postgresql://shaun:a128299239@localhost:5432/FSND-Capstone'
'''
database_path = 'postgresql://shaun:a128299239@localhost:5432/FSND-Capstone'
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    '''
    binds a flask application and a SQLAlchemy service
    '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    '''
    db.drop_all()
    db.create_all()
    db_init_records()
    '''
def db_drop_and_create_all():
    '''
    drops the database tables and starts fresh
    can be used to initialize a clean database
    '''
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    '''
    initialize the database with some records.
    '''

    new_actor = (Actor(
        name = 'Shaun',
        gender = 'Male',
        age = 30
        ))
    new_actor.insert()

    new_movie = (Movie(
        title = 'Shaun first super movie',
        release_date = date.today()
        ))
    new_movie.insert()
    
    new_act_movies = act_movies.insert().values(
        actor_id = new_actor.id,
        movie_id = new_movie.id
    )

    db.session.execute(new_act_movies) 
    db.session.commit()

#----------------------------------------------------------------------------#
# Association table for Actor and Movie in Many-To-Many relational database
#----------------------------------------------------------------------------#

act_movies = db.Table('act_movies',
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True)
)

#----------------------------------------------------------------------------#
# Actor Model 
#----------------------------------------------------------------------------#
class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable = False)
  gender = Column(String, nullable = False)
  age = Column(Integer, nullable = False)
  movies = db.relationship('Movie', secondary=act_movies, 
    backref=db.backref('actors', lazy=True))

  def __init__(self, name, gender, age):
    self.name = name
    self.gender = gender
    self.age = age

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name' : self.name,
      'gender': self.gender,
      'age': self.age
    }

#----------------------------------------------------------------------------#
# Movies Model 
#----------------------------------------------------------------------------#
class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String, nullable = False)
  release_date = Column(Date, nullable = False)

  def __init__(self, title, release_date) :
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title' : self.title,
      'release_date': self.release_date
    }