"""
Resource: Brevet
"""
from flask import Response, request
from flask_restful import Resource
from mongoengine import errors
from datetime import datetime
from json import dumps

# You need to implement this in database/models.py
from database.models import *

class Brevet_Resource(Resource):
    def get(self, id):
        try:
            return Response(Brevet.objects.get(id=str(id)).to_json(), mimetype="application/json", status=200)
        except:
            return Response(dumps({"Message": f"Object w/ oid {str(id)} not found in database!"}), status=404)
    def delete(self, id):
        try:
            Brevet.objects.get(id=str(id)).delete()
            return Response(dumps({"Message": f"Object w/ oid {str(id)} successfully deleted!"}), status=200)
        except:
            return Response(dumps({"Message": f"Object w/ oid {str(id)} not found in database!"}), status=404)
    def put(self, id):
        try:
            Brevet.objects(id=str(id)).update_one(
                set__length=6.28,
                set__start_time=datetime.now(),
                set__checkpoints=[
                    Checkpoint(
                        distance=6.28,
                        open_time = datetime.now(),
                        close_time = datetime.now()
                    )
                ]
            )
            return Response(dumps({"Message": f"Object w/ oid {str(id)} successfully updated!"}), status=200)
        except:
            return Response(dumps({"Message": f"Object w/ oid {str(id)} not found in database!"}), status=404)