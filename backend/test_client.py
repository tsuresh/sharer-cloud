import socketio

# standard Python
sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.on('*')
def catch_all(event, data):
    print(event)

sio.connect('ws://localhost:5000', wait_timeout = 10)