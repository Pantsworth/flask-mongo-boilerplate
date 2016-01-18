# DISCLAIMER: much of the initial code is a modified version of
# http://spapas.github.io/2014/06/30/rest-flask-mongodb-heroku/

import os
from flask import Flask, request
import flask_restful as restful
from flask.ext.pymongo import PyMongo
from flask import make_response, render_template
from bson.json_util import dumps
import json

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/rest";

app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def threshold_form():
    threshold = "Not Set"
    # database status
    root = flask_rest_service.resources.Root()
    root_test = flask_rest_service.resources.Root.get(root)

    return render_template('form.html', db_status=root_test, html_threshold=threshold, html_data=threshold)


@app.route('/threshold', methods=['GET', 'POST'])
def threshold_adjust():
    # get data from the form POST
    result = ""
    hello_world = "HELLO"
    threshold = request.form['threshold']
    try:
        latitude = float(request.form['lat'])
        longitude = float(request.form['long'])
    except ValueError:
        print "failed to load location"
        latitude = float(0.0)
        longitude = float(0.0)

    orientation = request.form['form-orientation']
    print "Threshold: ", threshold, "\nLocation: ", latitude, longitude, "\nOrientation: ", orientation

    # threshold input parsing
    if str(threshold.lower()) == "reset":
        print "Deleting data"
        mongo.db.readings.remove({})
    elif str(threshold).lower() == "add":
        jo = {'reading': 'location', 'latitude': latitude, 'longitude': longitude, 'orientation': orientation}
        mongo.db.readings.insert(jo)
        result = "Added New Record"

    elif str(threshold).lower()== "all":
        result = "Displaying All Records"
        for vals in mongo.db.readings.find({}):
            print "vals:", vals
            result += str(vals)
    else:
        try:
            threshold = float(threshold)
            if threshold < float(41):
                hello_world = "WORLD"
        except:
            threshold = "Invalid Input: Threshold Setting Failed"

    # database operations

    # for vals in mongo.db.readings.find({}):
    #     print "vals:", vals

    find_threshold = mongo.db.readings.find({"latitude": {"$gt": threshold}})
    for doc in mongo.db.readings.find({"latitude": {"$gt": threshold}}):
        print doc
        result += str(doc)

    if result == "":
        result = "No Records Found"

    # make a connection to our database
    reading = flask_rest_service.resources.ReadingList()
    reading_get = reading.get()

    # Database connection status
    root = flask_rest_service.resources.Root()
    root_test = flask_rest_service.resources.Root.get(root)

    # return data in a new version of the same page
    return render_template('form.html', html_helloworld=hello_world, db_status=root_test, html_threshold=threshold, html_data=result)


def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS

import flask_rest_service.resources
