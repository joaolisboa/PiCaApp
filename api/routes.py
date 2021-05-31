from __main__ import app
from flask import request

@app.route('/start', methods=['POST'])
def start():
    camera = app.config['SHARED'].camera
    requestData = request.get_json()
    camera.start(requestData, warmup=True)
    return ('', 200)

@app.route('/stop', methods=['POST'])
def stop():
    camera = app.config['SHARED'].camera
    camera.stop()
    return ('', 200)

@app.route('/capture-photo', methods=['POST'])
def capturePhoto():
    camera = app.config['SHARED'].camera
    filename = camera.action('capture').run()
    return (filename, 200)