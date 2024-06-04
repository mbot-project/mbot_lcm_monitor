# This file will start the LCM listener.

import lcm
import threading
from ..handlers.apriltag_handler import apriltag_handler

def lcm_listener():
    lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=0")
    lc.subscribe("MBOT_APRILTAG_ARRAY", apriltag_handler)
    try:
        while True:
            lc.handle()
    except KeyboardInterrupt:
        pass

def start_lcm_listener():
    lcm_thread = threading.Thread(target=lcm_listener)
    lcm_thread.daemon = True
    lcm_thread.start()
