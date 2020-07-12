import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from datetime import date
from models import setup_db, Actor, Movie, act_movies

casting_assistant_auth_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVuR2NFaHJia3I5akY2cmF0S25nQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA4NTkxOTc3ODY5MTAwNzg3NTkyIiwiYXVkIjpbIkNhc3RpbmctQWdlbmN5LUlkZW50aWZpZXIiLCJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NDU2MzkwNCwiZXhwIjoxNTk0NTcxMTA0LCJhenAiOiIwTXVycm9uQjNrZ2I4YVNhNUEzMVBRYzFMR1FtVmh1OSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.ekY61C7eAJN3fuzw1r5evh9XfMcmV3WnTkT7qibuv44a3Rne52WQMK2zXooinh_PPquQZdMvt01d-YQahGCtKTbf1nQcQxfil1ldD-BqOKFUxKCNcPPd5dgRtptSH0cXOO8k89erMSRvHYOaBzj-0qb-BkezZe347hMpHImDHFT4lIU0p-JV_bdHyTzD0XuwZnsEnRT8buBUXSiKGRgxjL6SeopVwO6WRkZ9kl4vzGxN5X9dB6zSzQPOi0JK_Aen4czmTS0PEso52bgdLIwQ3lweSIr-NCaVMyirz0vEF5r5UZpCtdSoQAsWa9yOVVUd36R3Qi8aTCnf1bp7Udvhaw'
executive_producer_auth_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVuR2NFaHJia3I5akY2cmF0S25nQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTEzODI1MDA0MDUxMjU0ODIzMjA2IiwiYXVkIjpbIkNhc3RpbmctQWdlbmN5LUlkZW50aWZpZXIiLCJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NDU2Mzg1MiwiZXhwIjoxNTk0NTcxMDUyLCJhenAiOiIwTXVycm9uQjNrZ2I4YVNhNUEzMVBRYzFMR1FtVmh1OSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.IyXHNlvrM3UPbV9L0FlUuPZL6L2DRUpskHZjTdEXFWpnXjogtMmrNqGsbrdYXWtStCqS6yGcrdfleJf-KJjKr56GlK5BiRkkQY5At5eYQrk5tSqixPVFS_oILxSQed6kvNVllk-eF6JIIoctx7nJfZrEk5eGxSdZwE33fxpf6fO84x9SNer9l_lY7rG1kWQdzWNl6aCc9D26McXWXzk9VPbJYxa6EaKNufsJYgohk-iHHRtVVuhLslEGNK2K7SsNzHXUtUlXM8Vg-E12sYTGabhx6NXpU0S2OUYrReCP56cWmh_droLvgz10bl4nHLBIqGtud7BofTWwy-ya46a3NA'

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
  
  #----------------------------------------------------------------------------#
  # Tests for /actors GET
  #----------------------------------------------------------------------------#
  def test_get_all_actors(self):
    """Test GET all actors."""
    res = self.client().get('/actors', headers = {'Authorization' : casting_assistant_auth_header})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) > 0)

  def test_error_401_get_all_actors(self):
    """Test GET all actors w/o Authorization."""
    res = self.client().get('/actors?page=1')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])
    self.assertEqual(data['message'], 'Authorization header is expected.')

  def test_error_404_get_actors(self):
    """Test Error GET all actors."""
    res = self.client().get('/actors?page=100', headers = {'Authorization' : executive_producer_auth_header})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertFalse(data['success'])
    self.assertEqual(data['message'] , 'resource not found')

  #----------------------------------------------------------------------------#
  # Tests for /actors POST
  #----------------------------------------------------------------------------#
  
  def test_create_new_actor(self):
    """Test POST new actor."""

    new_actor = {
        'name' : 'June',
        'gender': 'Female',
        'age' : "53"
    } 

    res = self.client().post('/actors', json = new_actor, headers = {'Authorization' : executive_producer_auth_header})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    
  def test_error_401_new_actor(self):
    """Test POST new actor w/o Authorization."""

    new_actor = {
        'name' : 'Ignatia',
        'gender': 'Female',
        'age' : "25"
    } 

    res = self.client().post('/actors', json = new_actor)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])
    self.assertEqual(data['message'], 'Authorization header is expected.')

  #----------------------------------------------------------------------------#
  # Tests for /actors PATCH
  #----------------------------------------------------------------------------#

  def test_edit_actor(self):
    """Test PATCH existing actors"""
    json_edit_actor_with_new_age = {
        'age' : 35
    } 
    res = self.client().patch('/actors/1', json = json_edit_actor_with_new_age, headers = {'Authorization' : executive_producer_auth_header})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertEqual(data['id'], 1)

  def test_error_400_edit_actor(self):
    """Test PATCH with non json body"""

    res = self.client().patch('/actors/152', headers = {'Authorization' : executive_producer_auth_header})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 400)
    self.assertFalse(data['success'])
    self.assertEqual(data['message'] , "bad request")

  #----------------------------------------------------------------------------#
  # Tests for /actors DELETE
  #----------------------------------------------------------------------------#
  
  def test_delete_actor(self):
    """Test DELETE existing actor"""
    res = self.client().delete('/actors/1', headers = {'Authorization' : executive_producer_auth_header})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])

  def test_error_422_delete_actor(self):
    """Test DELETE non existing actor"""
    res = self.client().delete('/actors/152', headers = {'Authorization' : executive_producer_auth_header})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertFalse(data['success'])
    self.assertEqual(data['message'] , 'unprocessable')

  #----------------------------------------------------------------------------#
  # Tests for /movies GET
  #----------------------------------------------------------------------------#

  def test_get_all_movies(self):
    """Test GET all movies."""
    res = self.client().get('/movies?page=1', headers = {'Authorization' : casting_assistant_auth_header})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(len(data['movies']) > 0)

  def test_error_401_get_all_movies(self):
    """Test GET all movies w/o Authorization."""
    res = self.client().get('/movies?page=1')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])
    self.assertEqual(data['message'], 'Authorization header is expected.')

  #----------------------------------------------------------------------------#
  # Tests for /movies POST
  #----------------------------------------------------------------------------#

  def test_create_new_movie(self):
    """Test POST new movie."""

    new_movie = {
        'title' : 'Swim',
        'release_date' : date.today()
    } 

    res = self.client().post('/movies', json = new_movie, headers = {'Authorization' : executive_producer_auth_header})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])

  def test_error_422_create_new_movie(self):
    """Test Error POST new movie."""

    movie_without_name = {
        'release_date' : date.today()
    } 

    res = self.client().post('/movies', json = movie_without_name, headers = {'Authorization' : executive_producer_auth_header})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertFalse(data['success'])
    self.assertEqual(data['message'], 'unprocessable')
  

  def test_405_if_actor_creation_not_allowed(self):
    res = self.client().post('/actors/555', json=self.new_actor, headers = {'Authorization' : executive_producer_auth_header})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 405)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'method not allowed')

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()