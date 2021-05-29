from Camera import Camera
from actions.Capture import Capture
from flask import Flask

app = Flask(__name__)
camera = Camera()
capture = Capture(camera = camera)

import api.routes

if __name__ == '__main__':
    app.run(debug=False, host='localhost')