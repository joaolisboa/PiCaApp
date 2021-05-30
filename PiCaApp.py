from Camera import Camera
from flask import Flask
import atexit
import logging
from gui.Window import Window
from State import State
import threading

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.warning('App started')

window = Window()
app = Flask(__name__)
camera = Camera()

# define routes
import api.routes

def exit_handler():
    camera.exit()
    logging.warning('App closed')

atexit.register(exit_handler)

def webserver(sharedState):
    app.config['SHARED'] = sharedState
    app.run(debug=True, host='localhost', use_reloader=False)

# run flask webserver in separate thread
def main():
    sharedState = State()
    uiThread = threading.Thread(target=webserver, args=(sharedState,))
    uiThread.start()

    window.render()
    uiThread.join()


if __name__ == '__main__':
    main()
