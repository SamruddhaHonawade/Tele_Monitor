from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    from .config import API_ID, API_HASH, PHONE_NUMBER
    app.config['API_ID'] = API_ID
    app.config['API_HASH'] = API_HASH
    app.config['PHONE_NUMBER'] = PHONE_NUMBER
    
    # Initialize routes
    from .routes import init_routes
    init_routes(app)
    
    return app