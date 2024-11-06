from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
from .config import Config

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Load config
app.config.from_object(Config)

# Initialize MySQL
mysql = MySQL(app)
