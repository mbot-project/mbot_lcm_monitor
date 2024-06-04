# This file creates and configures the Flask application. 

from flask import Flask, render_template
from .routes.apriltag_routes import apriltag_bp
from .utils.lcm_listener import start_lcm_listener

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(apriltag_bp, url_prefix='/apriltag')

    @app.route('/')
    def index():
        return render_template('home.html')
    
    # Start LCM listener in a separate thread
    start_lcm_listener()

    return app
