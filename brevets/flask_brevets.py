"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import os
import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
from pymongo import MongoClient
from bson import json_util

import logging

###
# Globals
###
app = flask.Flask(__name__)

# Hardcoded the environment variable. Shouldn't be a problem if running in Docker.
client = MongoClient('mongodb://mongo', 27017)
db = client.mydb

###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404

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
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

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

db_field_conversion = [
    "miles",
    "kilometers",
    "location",
    "open",
    "close"
]

# Accept form data from calc.html
@app.route("/_submit_times", methods = ['POST'])
def _submit_times():

    # Drop existing database. Don't want duplicates, or more than 20 records.
    db.drop_collection("brevets_collection")
    app.logger.debug("SUBMIT BUTTON CLICKED")

    # Need to make this a little friendlier for Python to work with
    vals = list(dict(request.form).values())

    for i in range(len(vals)):
        app.logger.debug(str(i) + " " + str(vals[i]))

    # THE DATA NEEDS TO BE HANDLED VERY RAPIDLY, AND SHOULD NOT BE STORED IN AN INTERMEDIARY DATA
    # STRUCTURE. I FOUND THIS OUT THE HARD WAY. PYTHON DICTIONARIES ARE NOT GOOD AT BEING PERSISTENT!

    # That said, we can do some pretty airtight math to figure out where everything should go.
    # Under the assumption that everything's received in a certain sequence, the dictionary keys are not
    # relevant.
    for i in range(20):
        db.brevets_collection.insert_one({
            "miles":        vals[i * 5],
            "kilometers":   vals[i * 5 + 1],
            "location":     vals[i * 5 + 2],
            "open":         vals[i * 5 + 3],
            "close":        vals[i * 5 + 4]
        })

    db.brevets_collection.insert_one({
        "brev_length": vals[100],
        "start_date":  vals[101]
    })

    '''
    for entry in list(db.brevets_collection.find()):
        app.logger.debug(entry)
    '''
    
    # This doesn't really do anything. I was getting 500 not implemented codes when not returning a string.
    return "200 OK"

# Transmit database data back to the server. It looks a little different from what was received, but can be
# parsed back into something workable in the frontend.
@app.route("/_retrieve", methods = ['GET'])
def _retrieve():
    # Pull the database data into something that can be reasoned with
    db_dictlist = list(db.brevets_collection.find())

    # Determine if the data can actually be reasoned with (count the elements)
    if db.brevets_collection.count_documents({}):
        # Convert from Mongo BSON to a string that JQuery can then make into a JSON object
        # app.logger.debug(json_util.dumps(db_dictlist))
        return flask.jsonify(empty={"empty": 0}, result=json_util.dumps(db_dictlist))
    else:
        # Tell the server the collection doesn't exist or is empty (basically the same thing in this case)
        return flask.jsonify(empty={"empty": 1})

#############

if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    PORT = os.environ["PORT"]
    print(f"Opening for global access on port {PORT}")
    app.run(port=PORT, host="0.0.0.0")
