import eventlet
eventlet.monkey_patch()

import gevent

from flask import Flask
import socketio
import eventlet
import eventlet.wsgi
from onset_detection import record_and_analyze_mic

sock = socketio.Server(async_mode='eventlet')
app = Flask(__name__)
is_recording = False

recording_thread = None

@app.route("/")
def hello():
    return "Yo"

@sock.on('connect')
def connect(sid, environ):
    print("connect", sid)

@sock.on('record')
def record(sid):
    print("Start recording")
    global recording_thread
    recording_thread = eventlet.spawn(start_recording)


def start_recording():
    is_recording = True
    generator = record_and_analyze_mic()
    generator.next()
    generator.send(is_recording)
    while (is_recording):
        ioi = next(generator)
        # print('ioi: {}', ioi)
    # for ioi in generator:
        # if ioi >= 0:
        #     print("boom")
        #     sock.emit('ioi', { 'ioi': ioi})
            # eventlet.sleep(0)
        resp = generator.send(is_recording)
        if resp >= 0:
            print('resp: {}', resp)
            sock.emit('ioi', { 'ioi': ioi})
            eventlet.sleep(0)


        eventlet.sleep(0)

@sock.on('stop_recording')
def stop_recording(sid):
    print("Stop Recording")
    global recording_thread
    eventlet.kill(recording_thread)

# @sock.on('message')
# def onMessage(sid, environ):
#     print("message received")
#     sock.emit('reply', {}, room=sid)

if __name__ == "__main__":
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sock, app)
    print("Starting server on port {}", 8000)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
