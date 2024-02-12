"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src.status import status

class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
      self.client = app.test_client()

    def test_create_a_counter(self):
         """It should create a counter"""
         client = app.test_client()
         result = client.post('/counters/foo')
         self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
         """It should update a counter"""
         # Try to update a counter that hasn't been created
         updated_result = self.client.put('/counters/up')
         self.assertEqual(updated_result.status_code, status.HTTP_409_CONFLICT)

         # Create a counter
         result = self.client.post('/counters/up')
         self.assertEqual(result.status_code, status.HTTP_201_CREATED)

         # Check the counter value as a baseline using json
         initial_json = result.json
         #get baseline
         baseline_value = initial_json.get('up', 0)

         # Update the counter
         updated_result = self.client.put('/counters/up')
         self.assertEqual(updated_result.status_code, status.HTTP_200_OK)

         # Check that the counter value is one more than the baseline one
         updated_json = updated_result.json
         updated_value = updated_json.get('up', 0)
         self.assertEqual(updated_value, baseline_value + 1)

    def test_read_a_counter(self):
        """It should read a counter"""
        # Try to read counter before its created
        read_result = self.client.get('/counters/read')
        self.assertEqual(read_result.status_code, status.HTTP_409_CONFLICT)

        # Create a counter
        result = self.client.post('/counters/read')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # Read the counter
        read_result = self.client.get('/counters/read')
        self.assertEqual(read_result.status_code, status.HTTP_200_OK)

        read_value = read_result.json.get('read', None)
        self.assertIsNotNone(read_value)
        self.assertEqual(read_value, 0)

