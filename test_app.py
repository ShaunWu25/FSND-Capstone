import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from datetime import date
from models import setup_db, Actor, Movie, act_movies

casting_assistant_auth_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVuR2NFaHJia3I5akY2cmF0S25nQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA4NTkxOTc3ODY5MTAwNzg3NTkyIiwiYXVkIjpbIkNhc3RpbmctQWdlbmN5LUlkZW50aWZpZXIiLCJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NDQ4MDQ2OCwiZXhwIjoxNTk0NDg3NjY4LCJhenAiOiIwTXVycm9uQjNrZ2I4YVNhNUEzMVBRYzFMR1FtVmh1OSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.ROu0kqcToPSSZm4Jzxd6eIY11wCpWfZaDsyVI8laQ4MJ4LDXmyLRw9QOBWvAfYI21gIBOR9O8ULepJ7o5YCLFbll6n5-lpquxfNsB8rcswYTIyREg5BVmP61o9PeO7QECP43KF34Pl1ic2PKvn095V_TFTLjyccBYhl8Dp3aZsfgmDx5F2EsSV8_6Wjdqg4LlHjxe2TEebVVGqt9p0GymQwIqD5Nkyo-2yIYYhAa7IimX1CvbgeBe0qKHhncdVcbkUCwxmc-nabr0s5V1LOMqDaSyPIJI9K6UwJriwiQh1akfMQ0hHRvgWt8pTQtpQzGSEb4tYqSN9-5UXxkrCthcg'
executive_producer_auth_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVuR2NFaHJia3I5akY2cmF0S25nQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTEzODI1MDA0MDUxMjU0ODIzMjA2IiwiYXVkIjpbIkNhc3RpbmctQWdlbmN5LUlkZW50aWZpZXIiLCJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NDQ4NDM0OCwiZXhwIjoxNTk0NDkxNTQ4LCJhenAiOiIwTXVycm9uQjNrZ2I4YVNhNUEzMVBRYzFMR1FtVmh1OSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.Be4VhvCdashgMAAor4y7F0UoLMqBRoc5oWoEptQuT2wQeFFmN0LWo3YwNCtAwCCRCRdZJHiy7spO7YHubb0Wpns0NdoEdnb1cZ2hRdfqB3oQJFwf4Xqjr7gL6cxBRhhomSp6sZ7vxMF0Sm3WtZ0jPt6-OLAAJPDl1Nb6hQqHG6JkbIexzvQIuepSoDwxq7lvnSy_wANfQCZvsgMKY85HRB1HUGD9Yc5Dcvtrf4UmCK3ATXwwcvBQiuiWRqYxSKA1ZHyRToCu6MMDUd6slRdZJbaEK9IxC2QS2O7h8uW0UoyCvO85wON7s2IEKrEg8fGgoFLFC6kyqm6zmvgi016QJQ'

class CastingAgencyTestCase(unittest.TestCase):
  """This class represents the ___ test case"""

  def setUp(self):
    """Executed before each test. Define test variables and initialize app."""
    self.app = create_app()
    self.client = self.app.test_client
    self.database_path = 'postgres://fgsdzdaogcqesw:af2c5a057da5d71b235a2f7850494bb0d4ee4930a041b28153ad0cc395e62567@ec2-54-236-169-55.compute-1.amazonaws.com:5432/d1t4destug4dco'
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
  '''
  def test_get_paginated_actors(self):
    res = self.client().get('/actors')
    data = json.loads(res.data)
    
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['total_actors'])
    self.assertTrue(len(data['actors']))
  '''
  def test_get_all_actors(self):
    """Test GET all actors."""
    res = self.client().get('/actors', headers = {'Authorization' : executive_producer_auth_header})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) > 0)
  '''
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
'''
# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()