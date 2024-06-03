from flask import Flask, render_template, jsonify
import lcm
from mbot_lcm_msgs.mbot_apriltag_array_t import mbot_apriltag_array_t
import threading
import time

app = Flask(__name__)
apriltag_data = {}
apriltag_last_update_time = 0

# apriltag_data = {
#     "array_size": 0,
#     "detections": [detection1, detection2]
# }

def apriltag_handler(channel, data):
    global apriltag_data, apriltag_last_update_time
    msg = mbot_apriltag_array_t.decode(data)
    apriltag_last_update_time = time.time()  # Update the timestamp
    apriltag_data["array_size"] = msg.array_size
    if msg.array_size != 0:
        detections = []
        for detection in msg.detections:
            detections.append({
                'tag_id': detection.tag_id,
                'pose': [detection.pose.x, detection.pose.y, detection.pose.z],
                'angles_rpy': detection.pose.angles_rpy,
            })
        apriltag_data["detections"] = detections

def lcm_listener():
    lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=0")
    apiltag_sub = lc.subscribe("MBOT_APRILTAG_ARRAY", apriltag_handler)
    try:
        while True:
            lc.handle()
    except KeyboardInterrupt:
        pass

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/status')
def get_status():
    global apriltag_last_update_time
    current_time = time.time()
    status = "on" if (current_time - apriltag_last_update_time) <= 3 else "off"
    return jsonify({"apriltag_status": status})

@app.route('/apriltag_msg')
def apriltag_msg():
    return render_template('apriltag_msg.html')

@app.route('/apriltag_data')
def apriltag_data_route():
    return jsonify(apriltag_data)

if __name__ == '__main__':
    lcm_thread = threading.Thread(target=lcm_listener)
    lcm_thread.daemon = True
    lcm_thread.start()
    # not having host='0.0.0.0' here for network security reason
    # vscode will auto forward ports from remote to local
    app.run(debug=True, port=5002)
