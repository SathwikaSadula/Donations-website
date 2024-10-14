from flask import Flask, jsonify, request
from flask_cors import CORS

from display_requests import requests_bp
from donations import donations_bp
from fulfill_Donations import fulfill_donations_bp
from login import auth_bp
from new_item_req import new_item_req_bp
from new_user import create_party_bp

app = Flask(__name__)
app.register_blueprint(requests_bp)
app.register_blueprint(donations_bp)
app.register_blueprint(fulfill_donations_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(new_item_req_bp)
app.register_blueprint(create_party_bp)

CORS(app)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'Pong!'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)