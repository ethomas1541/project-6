"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import os
import flask
from flask import request
from requests import get, post
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
from bson import json_util

import logging

###
# Globals
###
app = flask.Flask(__name__)

API_PORT = os.environ["API_PORT"]
API_ADDR = os.environ["API_ADDR"]

###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html', api_addr=os.environ["API_ADDR"])

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404

@app.route("/_retrieve", methods=['GET'])
def get_from_api():
    # Use HTTP to get a JSON from the API.
    req = get(f"http://{API_ADDR}:{API_PORT}/api/brevets")
    # app.logger.debug(req.content)
    return req.content

@app.route("/_submit", methods=['POST'])
def send_to_api():
    # Use HTTP to post a JSON to the API
    post(f"http://{API_ADDR}:{API_PORT}/api/brevets", json=request.get_json(force=True))
    return "200 OK"

@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)

    # Brevet distance and start date
    brev_dist = request.args.get('brev_dist', 200, type=int)
    start_date = request.args.get('start_date', type = str)

    # Arrow object from start_date string
    start_arrow = arrow.get(start_date)

    # Ideal case, for when all data is valid
    # ecode 0 signifies no error at all
    try:
        open_time = acp_times.open_time(km, brev_dist, start_arrow).format('YYYY-MM-DDTHH:mm')
        close_time = acp_times.close_time(km, brev_dist, start_arrow).format('YYYY-MM-DDTHH:mm')
        result = {"open": open_time, "close": close_time, "ecode": 0}
        return flask.jsonify(result=result)
    
    # Send back an unchanged version of the open and close fields' initial data.
    # Send back an error code the frontend can translate to a human-readable error message
    except OverflowError:
        result = {"open": "mm/dd/yyyy --:-- --", "close": "mm/dd/yyyy --:-- --", "ecode": 1}
        return flask.jsonify(result=result)
    except ArithmeticError:
        result = {"open": "mm/dd/yyyy --:-- --", "close": "mm/dd/yyyy --:-- --", "ecode": 2}
        return flask.jsonify(result=result)

#############

if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    PORT = os.environ["PORT"]
    DEBUG = os.environ["DEBUG"]
    print(f"Opening for global access on port {PORT}")
    app.run(debug=DEBUG, port=PORT, host="0.0.0.0")
