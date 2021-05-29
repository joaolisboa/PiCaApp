from Camera import Camera
from actions.Capture import Capture
from flask import Flask
import atexit
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.warning('App started')

app = Flask(__name__)
camera = Camera()
capture = Capture(camera = camera)

import api.routes

def exit_handler():
    camera.stop()
    logging.warning('App closed')

if __name__ == '__main__':
    app.run(debug=False, host='localhost')

atexit.register(exit_handler)