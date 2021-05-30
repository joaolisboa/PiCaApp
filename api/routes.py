from __main__ import app, camera
from actions.Action import Action
from flask import request

@app.route('/start', methods=['POST'])
def start():
    requestData = request.get_json()
    camera.start(requestData, warmup=True)
    return ('', 200)

@app.route('/stop', methods=['POST'])
def stop():
    camera.stop()
    return ('', 200)

@app.route('/capture-photo', methods=['POST'])
def capturePhoto():
    filename = Action('capture').run()
    return (filename, 200)