import unittest
from app import app
from pymongo import MongoClient
import os
import json

class MusicManagerTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Setup test database
        mongo_uri = f"mongodb://{os.environ.get('MONGO_USERNAME')}:{os.environ.get('MONGO_PASSWORD')}@{os.environ.get('MONGO_HOST')}:{os.environ.get('MONGO_PORT', 27017)}/test_db"
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client.test_db

    def tearDown(self):
        # Clean up the test database
        self.mongo_client.drop_database('test_db')
        self.mongo_client.close()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_singer(self):
        response = self.client.post('/add_singer', data={'name': 'Test Singer'})
        self.assertEqual(response.status_code, 302)  # Redirect status code
        
        # Verify singer was added
        singer = self.db.singers.find_one({'name': 'Test Singer'})
        self.assertIsNotNone(singer)
        self.assertEqual(singer['name'], 'Test Singer')

    def test_add_song(self):
        # First add a singer
        singer_result = self.db.singers.insert_one({'name': 'Test Singer'})
        singer_id = str(singer_result.inserted_id)

        # Then add a song
        response = self.client.post('/add_song', data={
            'title': 'Test Song',
            'singers': [singer_id]
        })
        self.assertEqual(response.status_code, 302)

        # Verify song was added
        song = self.db.songs.find_one({'title': 'Test Song'})
        self.assertIsNotNone(song)
        self.assertEqual(song['title'], 'Test Song')
        self.assertEqual(song['singer_ids'], [singer_id])

    def test_remove_singer(self):
        # Add a singer first
        result = self.db.singers.insert_one({'name': 'Test Singer'})
        singer_id = str(result.inserted_id)

        # Remove the singer
        response = self.client.get(f'/remove_singer/{singer_id}')
        self.assertEqual(response.status_code, 302)

        # Verify singer was removed
        singer = self.db.singers.find_one({'_id': result.inserted_id})
        self.assertIsNone(singer)

if __name__ == '__main__':
    unittest.main()