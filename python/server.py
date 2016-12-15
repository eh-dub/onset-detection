from flask import Flask
import socketio
import eventlet
import eventlet.wsgi
from onset_detection import record_and_analyze_mic

sock = socketio.Server()
app = Flask(__name__)

@app.route("/")
def hello():
    return "Yo"

@sock.on('connect')
def connect(sid, environ):
    print("connect", sid)

# @sock.on('boop')
# def boop(sid, environ):
#     print("IVE BEEN BOOPED")
#     sock.emit('reply', {}, room=sid)

@sock.on('record')
def record(sid):
    print("Start recording")
    record_and_analyze_mic()
    sock.emit('done recording', {}, room=sid);


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
