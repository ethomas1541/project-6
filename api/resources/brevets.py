"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource
from datetime import datetime
from json import dumps

# You need to implement this in database/models.py
from database.models import *

# MongoEngine queries:
# Brevet.objects() : similar to find_all. Returns a MongoEngine query
# Brevet(...).save() : creates new brevet
# Brevet.objects.get(id=...) : similar to find_one

# Two options when returning responses:
#
# return Response(json_object, mimetype="application/json", status=200)
# return python_dict, 200
#
# Why would you need both?
# Flask-RESTful's default behavior:
# Return python dictionary and status code,
# it will serialize the dictionary as a JSON.
#
# MongoEngine's objects() has a .to_json() but not a .to_dict(),
# So when you're returning a brevet / brevets, you need to convert
# it from a MongoEngine query object to a JSON and send back the JSON
# directly instead of letting Flask-RESTful attempt to convert it to a
# JSON for you.

class Brevets_Resource(Resource):
    def post(self):
        vals = list(dict(request.form).values())
        new_brev = Brevet(
            length=3.14,
            start_time=datetime.now(),
            checkpoints=[
                Checkpoint(
                    distance=3.14,
                    open_time=datetime.now(),
                    close_time=datetime.now()
                )
            ]
        )
        new_brev.save()
        return Response(dumps({"Message": f"Object w/ oid {str(new_brev.id)} successfully created!"}), status=201)
    def get(self):
        return Response(Brevet.objects.to_json(), mimetype="application/json", status=200)