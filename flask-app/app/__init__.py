# This file creates and configures the Flask application.

from flask import Flask
from .config import Config

def create_app():
    # Initialize the Flask app
    app = Flask(__name__)
    
    # Load configuration from the Config class
    app.config.from_object(Config)
    
    # Register routes (Blueprints)
    from .routes.health import health_bp
    from .routes.films import films_bp
    from .routes.customers import customers_bp
    from .routes.rentals import rentals_bp
    from .routes.payments import payments_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(films_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(rentals_bp)
    app.register_blueprint(payments_bp)
    
    return app
