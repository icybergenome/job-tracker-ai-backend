from flask import Flask
from redis import Redis
from rq import Queue

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object('app.config.Config')

# Initialize Redis and RQ
redis_conn = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=0)
queue = Queue(connection=redis_conn)

# Import routes
from app.routes import *