import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import APP
from database.models import setup_db, Movies, Actors, create_drop_tables

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    create_drop_tables()
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.executive_producer = os.environ['EXECUTIVE_PRODUCER']
        self.casting_assistant = os.environ['CASTING_ASSISTANT']
        
        self.new_movie = {
            'title': 'kingdom',
            'release_date': '25-10-2019'
        }

        self.new_actor = {
            'name': 'mennsa shelaby',
            'age': 30,
            'gender': 'female'
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def header(self, token):
        return {'Content-Type': 'application/json', 'Authorization': 'bearer ' + token}
    
    ###### Test endpoints for success and error behavior

    # POST 
    ## Success behavior
    def test_create_movie(self):
        self.client().post('/movies', headers=self.header(self.executive_producer), json=self.new_movie)
        res = self.client().post('/movies', headers=self.header(self.executive_producer), json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_create_actor(self):
        self.client().post('/actors', headers=self.header(self.executive_producer), json=self.new_actor)
        res = self.client().post('/actors', headers=self.header(self.executive_producer), json=self.new_actor)
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    ## Error behavior
    def test_401_post_movie_without_auth_header(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    
    def test_401_post_actor_without_auth_header(self):
        res = self.client().post('/actors', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    ###----------------------------------------------------------------------------------------------------------
    # GET
    ## Success behavior

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.header(self.casting_assistant))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.header(self.casting_assistant))
        data = json.loads(res.data)
        self.assertTrue(data['actors'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    ## Error behavior
    def test_401_get_movies_without_auth_header(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_get_actors_without_auth_header(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    ###----------------------------------------------------------------------------------------------------------
    # # PATCH
    ## Success behavior
    def test_update_movie_partially(self):
        res = self.client().patch('/movies/1', headers=self.header(self.executive_producer), json={'title': 'new-title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_update_actor_partially(self):
        res = self.client().patch('/actors/1', headers=self.header(self.executive_producer), json={'name': 'new-name'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Error behavior
    def test_401_update_movie_partially_without_auth_header(self):
        res = self.client().patch('/movies/1', json={'title': 'new-title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_update_actor_partially_without_auth_header(self):
        res = self.client().patch('/actors/1', json={'title': 'new-title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    ###----------------------------------------------------------------------------------------------------------
    # DELETE
    ## Success behavior

    def test_delete_movie(self):
        res = self.client().delete('/movies/2', headers=self.header(self.executive_producer))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors(self):
        res = self.client().delete('/actors/2', headers=self.header(self.executive_producer))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    ## Error behavior
    def test_401_delete_movie_without_auth_header(self):
        res = self.client().delete('/movies/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_delete_actors_without_auth_header(self):
        res = self.client().delete('/actors/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #####---------------------------------------------------------------------------------------#####

    # Test role-based access control

    ## EXECUTIVE PRODUCER 
    def test_get_movies_with_executive_producer(self):
        res = self.client().get('/movies', headers=self.header(self.executive_producer))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_actors_with_executive_producer(self):
        res = self.client().get('/actors', headers=self.header(self.executive_producer))
        data = json.loads(res.data)
        self.assertTrue(data['actors'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    ## CASTING ASSISTANT
    def test_get_movies_with_casting_assistant(self):
        res = self.client().get('/movies', headers=self.header(self.casting_assistant))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_actors_with_casting_assistant(self):
        res = self.client().get('/actors', headers=self.header(self.casting_assistant))
        data = json.loads(res.data)
        self.assertTrue(data['actors'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()