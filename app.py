#!/usr/bin/env python

from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
import flightxml
import apisecrets as API


app = Flask(__name__)

wx_obs = []

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


# TODO: Delete below function
@app.route('/av-data/api/v1.0/wx_obs', methods=['GET'])
@auth.login_required
def get_wx():
    return jsonify({'wx_obs': wx_obs})



# TODO: Delete below function
@app.route('/av-data/api/v1.0/wx_obs/<int:obs_id>', methods=['GET'])
@auth.login_required
def get_wx_obs(obs_id):
    wx = [obs for obs in wx_obs if obs['id'] == obs_id]
    if len(wx) == 0:
        abort(404)
    return jsonify({'wx_obs': wx})


@app.route('/av-data/api/v1.0/wx_obs', methods=['POST'])
@auth.login_required
def create_wx_obs():
    if not request.json or not 'airport_code' in request.json:
        abort(400)
    if not wx_obs:
        wx = {
            'id': 0,
            'ob': flightxml.get_airport_wx(request.json['airport_code'])
        }
    else:
        wx = {
            'id': wx_obs[-1]['id'] + 1,
            'ob': flightxml.get_airport_wx(request.json['airport_code'])
        }

    wx_obs.append(wx)
    return jsonify({'id': wx['id'], 'wx_obs': wx['ob']})

if __name__ == '__main__':
    app.run(debug=True)
