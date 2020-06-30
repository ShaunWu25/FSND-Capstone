import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from datetime import date
from models import setup_db, Actor, Movie, act_movies

class CastingAgencyTestCase(unittest.TestCase):
  """This class represents the ___ test case"""

  def setUp(self):
    """Executed before each test. Define test variables and initialize app."""
    self.app = create_app()
    self.client = self.app.test_client
    self.database_path = 'postgresql://shaun:a128299239@localhost:5432/FSND-Capstone'
    setup_db(self.app, self.database_path)

    self.new_actor = {
      'name': "Erny",
      'gender': 'Male',
      'age': 39
    }

    # binds the app to the current context
    with self.app.app_context():
        self.db = SQLAlchemy()
        self.db.init_app(self.app)
        # create all tables
        self.db.create_all()
    

  def tearDown(self):
    """Executed after reach test"""
    pass

  def test_get_paginated_actors(self):
    res = self.client().get('/actors')
    data = json.loads(res.data)
    
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['total_actors'])
    self.assertTrue(len(data['actors']))

  def test_404_sent_requesting_beyond_valid_page(self):
    res = self.client().get('/actors?page=500', json={'age':25})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')

  def test_update_actor_age(self):
    res = self.client().patch('/actors/2', json={'age':95})
    data = json.loads(res.data)
    actor = Actor.query.filter(Actor.id == 2).one_or_none()

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(actor.format()['age'], 95)

  def test_400_for_failed_update(self):
    res = self.client().patch('/actors/2')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'bad request')

  def test_delete_actor(self):
    res = self.client().delete('/actors/16')
    data = json.loads(res.data)

    actor = Actor.query.filter(Actor.id == 1).one_or_none()

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['deleted'], 16)
    self.assertTrue(data['total_actors'])
    self.assertTrue(len(data['actors']))
    self.assertEqual(actor, None)

  def test_422_if_actor_does_not_exist(self):
    res = self.client().delete('/actors/1000')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')

  def test_create_new_actor(self):
    res = self.client().post('/actors', json=self.new_actor)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['created'])
    self.assertTrue(len(data['actors']))

  def test_405_if_actor_creation_not_allowed(self):
    res = self.client().post('/actors/555', json=self.new_actor)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 405)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'method not allowed')

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()