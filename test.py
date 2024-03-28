import unittest
import subprocess
import os
import requests
import time
import signal

class TestFlaskApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        
        os.environ['FLASK_APP'] = 'app'
        os.environ['FLASK_RUN_PORT'] = '5000'
        os.environ['FLASK_ENV'] = 'development'
        os.system('sudo docker build -t my-flask-app .')
        # Start the Flask app in a separate process
        cls.flask_process = subprocess.Popen('sudo docker run -p 5000:5000 --name docker-flask my-flask-app'.split(' '))
        # Wait for the Flask app to start
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        # Terminate the Flask app process by sending a SIGINT signal to the subprocess
        # cls.flask_process.terominat()
        # cls.flask_process.wait()
        os.kill(cls.flask_process.pid, signal.SIGINT)
        time.sleep(3)
        os.system('sudo docker container rm docker-flask')
        os.system('sudo docker image rm my-flask-app --force')

    def test_flask_app(self):
        """Test the Flask endpoint."""
        response = requests.post('http://localhost:5000/score', json={'text': 'This is AML HW 3', 'threshold': 0.5})
        self.assertEqual(response.status_code, 200)
        self.assertIn('prediction', response.json())
        self.assertIn('propensity', response.json())


if __name__ == '__main__':
    unittest.main()
