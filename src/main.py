"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from datastructures import Queue
from sms import send_msg
#from models import Person

queue = Queue()
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/queue', methods=['GET'])
def get_queue():
    current_queue = queue.get_queue()
    size_of_queue = queue.size()
    response_body = {
        "queue": current_queue,
        "size": f"There are {size_of_queue} people in the queue",
        "next": f"Next is {current_queue[0]}" if size_of_queue else "Empty queue"
    }
    return jsonify(response_body), 200

@app.route('/queue', methods=['POST'])
def post_queue():
    request_body = request.get_json()
    queue.enqueue(request_body)
    response_body = {
        "queue": queue.get_queue(),
        "size": f"There are {queue.size()} people in the queue",
        "added": f"{queue.get_queue()[-1]['name']} was added to the queue"
    }
    return jsonify(response_body), 200

@app.route('/queue', methods=['DELETE'])
def delete_queue():
    called_person = queue.dequeue()
    current_queue = queue.get_queue()
    size = queue.size()
    send_msg(body=f"Hi, {called_person['name']}, your table is ready")

    response_body = {
        "called person": f"Is {called_person['name']}'s turn",
        "queue": current_queue,
        "size": f"There are {size} people in the queue",
        "next": f"Next is {current_queue[0]}" if size else "Empty queue"
    }
    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
