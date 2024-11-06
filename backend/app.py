# backend/app.py

from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
# Allow CORS for specific origins
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

# Configure MySQL database settings
app.config.from_object('backend.config.Config')

# Initialize MySQL
mysql = MySQL(app)

# Import routes after initializing the app to avoid circular imports
from backend.routes import api_blueprint

# Register the blueprint for your routes
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
