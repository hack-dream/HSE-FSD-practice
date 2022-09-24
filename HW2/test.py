import unittest
from app import app

class Tester(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_exception(self):
        # wrong method
        response = self.app.post('/hello') 
        self.assertEqual(response.status_code, 405)
        response = self.app.get('/set')
        self.assertEqual(response.status_code, 405)
        response = self.app.put('/set')
        self.assertEqual(response.status_code, 405)
        response = self.app.post('/get/key')
        self.assertEqual(response.status_code, 405)
        response = self.app.delete('/get/key')
        self.assertEqual(response.status_code, 405)
        response = self.app.get('/devide')
        self.assertEqual(response.status_code, 405)

        # wrong route
        response = self.app.get('/wrong_route')
        self.assertEqual(response.status_code, 405)

    def test_hello(self):
        # ok
        response = self.app.get('/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "text/plain")
        self.assertEqual(response.get_data(as_text=True), "HSE One Love!")

    def test_set(self):
        # ok
        response = self.app.post('/set',
                                 headers={"Content-Type": "application/json"},
                                 json={"key": "key1", "value": "value1"})
        self.assertEqual(response.status_code, 200)

        response = self.app.post('/set',
                                 headers={"Content-Type": "application/json"},
                                 json={"key": "key1", "value": "value1"})
        self.assertEqual(response.status_code, 200)

        # wrong content-type
        response = self.app.post('/set', headers={"Content-Type": "text/plain"})
        self.assertEqual(response.status_code, 415)

        # wrong key-value json
        response = self.app.post('/set',
                                 headers={"Content-Type": "application/json"},
                                 json={})
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/set',
                                 headers={"Content-Type": "application/json"},
                                 json={"key": "key1"})
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/set',
                                 headers={"Content-Type": "application/json"},
                                 json={"value": "value1"})
        self.assertEqual(response.status_code, 400)

    def test_get(self):
        # prepare value
        response = self.app.post('/set',
                                 headers={"Content-Type": "application/json"},
                                 json={"key": "key1", "value": "value1"})
        self.assertEqual(response.status_code, 200)
        
        # ok before update
        response = self.app.get('/get/key1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json, {"key": "key1", "value": "value1"})

        # update value
        response = self.app.post('/set',
                                 headers={"Content-Type": "application/json"},
                                 json={"key": "key1", "value": "value2"})

        # ok after update
        response = self.app.get('/get/key1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json, {"key": "key1", "value": "value2"})

        # nonexistent key
        response = self.app.get('/get/nonexistentkey')
        self.assertEqual(response.status_code, 404)


    def test_devide(self):
        # ok
        response = self.app.post('/devide',
                                 headers={"Content-Type": "application/json"},
                                 json={"dividend": 15, "divider": 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/plain')
        self.assertEqual(response.get_data(as_text=True), '1.5')
        
        # wrong content-type
        response = self.app.post('/devide',
                                 headers={})
        self.assertEqual(response.status_code, 415)
        
        response = self.app.post('/devide',
                                 headers={"Content-Type": "text/plain"})
        self.assertEqual(response.status_code, 415)

        # wrong dividend-divider values
        response = self.app.post('/devide',
                                 headers={"Content-Type": "application/json"},
                                 json={})
        self.assertEqual(response.status_code, 400)
        
        response = self.app.post('/devide',
                                 headers={"Content-Type": "application/json"},
                                 json={"dividend": 1})
        self.assertEqual(response.status_code, 400)
        
        response = self.app.post('/devide',
                                 headers={"Content-Type": "application/json"},
                                 json={"divider": 2})
        self.assertEqual(response.status_code, 400)
        
        # div 0
        response = self.app.post('/devide',
                                 headers={"Content-Type": "application/json"},
                                 json={"dividend": 1, "divider": 0})
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()