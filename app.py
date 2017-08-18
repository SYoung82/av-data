#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request
import flightxml


app = Flask(__name__)

wx_obs = []


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/av-data/api/v1.0/wx_obs', methods=['GET'])
def get_wx():
    return jsonify({'wx_obs': wx_obs})


@app.route('/av-data/api/v1.0/wx_obs/<int:obs_id>', methods=['GET'])
def get_wx_obs(obs_id):
    wx = [obs for obs in wx_obs if obs['id'] == obs_id]
    if len(wx) == 0:
        abort(404)
    return jsonify({'wx_obs': wx})


@app.route('/av-data/api/v1.0/wx_obs', methods=['POST'])
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
