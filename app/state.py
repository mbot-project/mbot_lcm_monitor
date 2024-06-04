# This file contains the State Class
# It tracks the status of LCM messages
# If there is no message triggers the handler
# It will set the status to "off"

import time

class State:
    def __init__(self):
        self.last_update_time = 0
        self.status = "off"

    def update_time(self):
        self.last_update_time = time.time()

    def get_time(self):
        return self.last_update_time

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

apriltag_state = State()
