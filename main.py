import lcm
import time
from threading import Thread, Event
from flask import Flask, render_template
from flask_socketio import SocketIO
from handler import message_handler, get_status

stop_event = Event()
update_rate = 5 # Update rate Hz

def lcm_handle_loop(lc):
    while not stop_event.is_set():
        try:
            lc.handle_timeout(1000)  # Timeout set to 1000ms
        except Exception as e:
            print(f"Error in LCM handle loop: {e}")

def status_update_loop(socketio):
    while not stop_event.is_set():
        status = get_status()
        socketio.emit('status_update', status)
        time.sleep(1/update_rate)  # webpage update rate

def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app)

    @app.route('/')
    def index():
        return render_template('home.html')

    return app, socketio

if __name__ == '__main__':
    lc = lcm.LCM()
    # Subscribe to LCM channels and handle messages
    subscription = lc.subscribe(".*", message_handler)

    # Create and run the Flask application in the main thread
    app, socketio = create_app()

    # Start the LCM handle loop thread
    lcm_thread = Thread(target=lcm_handle_loop, args=(lc,))
    lcm_thread.daemon = True
    lcm_thread.start()

    # Start the status update loop thread
    status_thread = Thread(target=status_update_loop, args=(socketio,))
    status_thread.daemon = True
    status_thread.start()

    try:
        socketio.run(app, debug=True, port=5002)
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
        stop_event.set()
        lcm_thread.join()
        status_thread.join()
        lc.unsubscribe(subscription)
        print("Exited cleanly.")
