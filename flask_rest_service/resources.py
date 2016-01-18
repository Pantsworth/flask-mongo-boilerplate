# DISCLAIMER: much of the initial code is a modified version of
# http://spapas.github.io/2014/06/30/rest-flask-mongodb-heroku/


import json
from flask import request, abort, render_template
import flask_restful as restful
from flask.ext.restful import reqparse
from flask_rest_service import app, api, mongo
from bson.objectid import ObjectId


class ReadingList(restful.Resource):
    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('reading', type=str)
        super(ReadingList, self).__init__()

    def get(self):
        return  [x for x in mongo.db.readings.find()]

    def post(self):
        args = self.parser.parse_args()
        if not args['reading']:
            abort(400)

        jo = json.loads(args['reading'])
        reading_id = mongo.db.readings.insert(jo)
        return mongo.db.readings.find_one({"_id": reading_id})


class Reading(restful.Resource):
    def get(self, reading_id):
        return mongo.db.readings.find_one_or_404({"_id": reading_id})

    def delete(self, reading_id):
        mongo.db.readings.find_one_or_404({"_id": reading_id})
        mongo.db.readings.remove({"_id": reading_id})
        return '', 204

# class Locations(restful.Resource):
#     def __init__(self, *args, **kwargs):
#         self.parser = reqparse.RequestParser()
#         self.parser.add_argument('reading', type=str)
#         super(Locations, self).__init__()
#
#     def get(self):
#         return  [x for x in mongo.db.readings.find()]
#
#     def post(self):
#         args = self.parser.parse_args()
#         if not args['reading']:
#             abort(400)
#
#         jo = json.loads(args['reading'])
#         reading_id = mongo.db.readings.insert(jo)
#         return mongo.db.readings.find_one({"_id": reading_id})


class Root(restful.Resource):
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }


class Add(restful.Resource):
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }

api.add_resource(Root, '/')
api.add_resource(ReadingList, '/readings/')
api.add_resource(Reading, '/readings/<ObjectId:reading_id>')