# This file contains the routes related to Apriltag messages.

from flask import Blueprint, render_template, jsonify
from ..handlers.apriltag_handler import apriltag_data
from ..state import apriltag_state
import time

apriltag_bp = Blueprint('apriltag', __name__)

@apriltag_bp.route('/status')
def get_status():
    current_time = time.time()
    if (current_time - apriltag_state.last_update_time) > 3:
        apriltag_state.status = "off"
    return jsonify({"apriltag_status": apriltag_state.status})

@apriltag_bp.route('/board')
def board():
    return render_template('apriltag_board.html')

@apriltag_bp.route('/data')
def get_data():
    return jsonify(apriltag_data)
