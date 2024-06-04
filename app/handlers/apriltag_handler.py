# Define the handler for Apriltag messages.

import time
from mbot_lcm_msgs.mbot_apriltag_array_t import mbot_apriltag_array_t
from ..state import apriltag_state

apriltag_data = {}

def apriltag_handler(channel, data):
    global apriltag_data
    msg = mbot_apriltag_array_t.decode(data)
    apriltag_state.update_time()
    apriltag_state.set_status("on")
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
