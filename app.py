#!/usr/bin/env python

from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin
import flightxml
import apisecrets as API


app = Flask(__name__)
CORS(app)

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'guest':
        return API.GUEST_PASSWORD
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/av-data/api/v1.0/wx_obs', methods=['POST'])
def create_wx_obs():
    if not request.json or not 'airport_code' in request.json:
        abort(400)
    else:
        wx = {
            'ob': flightxml.get_airport_wx(request.json['airport_code'])
        }

    return jsonify({'wx': wx['ob']})


@app.route('/av-data/api/v1.0/aircraft_enroute', methods=['POST'])
def get_enroute_aircraft():
    if not request.json or not 'airport_code' in request.json:
        abort(400)
    else:
        aircraft = {
            'aircraft': flightxml.get_enroute_aircraft(request.json['airport_code'])
        }

    return jsonify({'aircraft': aircraft['aircraft']})


@app.route('/av-data/api/v1.0/aircraft_departures', methods=['POST'])
def get_departure_aircraft():
    if not request.json or not 'airport_code' in request.json:
        abort(400)
    else:
        aircraft = {
            'aircraft': flightxml.get_departure_aircraft(request.json['airport_code'])
        }

    return jsonify({'aircraft': aircraft['aircraft']})


@app.route('/av-data/api/v1.0/aircraft_arrivals', methods=['POST'])
def get_arrival_aircraft():
    if not request.json or not 'airport_code' in request.json:
        abort(400)
    else:
        aircraft = {
            'aircraft': flightxml.get_arrival_aircraft(request.json['airport_code'])
        }

    return jsonify({'aircraft': aircraft['aircraft']})


if __name__ == '__main__':
    app.run(debug=True, port=33507)
