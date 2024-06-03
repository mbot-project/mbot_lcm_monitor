from flask import Flask, render_template, jsonify
import lcm
from mbot_lcm_msgs.mbot_apriltag_array_t import mbot_apriltag_array_t
from mbot_lcm_msgs.mbot_apriltag_t import mbot_apriltag_t
import threading

app = Flask(__name__)
lcm_data = {}

def lcm_handler(channel, data):
    global lcm_data
    msg = mbot_apriltag_array_t.decode(data)
    if msg.array_size == 0:
        lcm_data[channel] = {
            'tag_id': -1
        }
    else:
        detections = []
        for detection in msg.detections:
            detections.append({
                'tag_id': detection.tag_id,
                'pose': {
                    'x': detection.pose.x,
                    'y': detection.pose.y,
                    'z': detection.pose.z
                }
            })
        lcm_data[channel] = {
            'utime': msg.utime,
            'array_size': msg.array_size,
            'detections': detections
        }

def lcm_listener():
    lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=0")
    subscription = lc.subscribe("MBOT_APRILTAG_ARRAY", lcm_handler)
    try:
        while True:
            lc.handle()
    except KeyboardInterrupt:
        pass

@app.route('/lcm_monitor')
def index():
    return render_template('index.html')

@app.route('/latest_lcm')
def get_lcm_data():
    return jsonify(lcm_data)

if __name__ == '__main__':
    lcm_thread = threading.Thread(target=lcm_listener)
    lcm_thread.daemon = True
    lcm_thread.start()
    app.run(debug=True, host='0.0.0.0', port=5002)
