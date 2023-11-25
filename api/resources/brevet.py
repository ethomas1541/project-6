"""
Resource: Brevet
"""
from flask import Response, request, jsonify
from flask_restful import Resource
from mongoengine import errors
from datetime import datetime
from json import dumps, loads

# You need to implement this in database/models.py
from database.models import *

def StringFromUnixTime(timestamp: str) -> str:
    return datetime.utcfromtimestamp(float(timestamp)/1000).strftime("%Y-%m-%dT%H:%M")

class Brevet_Resource(Resource):
    # GET method of this URL
    def get(self, id):
        try:
            # Load up a JSON of the requested brevet
            resp_dict = loads(Brevet.objects.get(id=str(id)).to_json())

            # Convert all UNIX timestamps to date strings that can be used in the frontend
            resp_dict["start_time"] = StringFromUnixTime(resp_dict["start_time"]["$date"])
            for chk in resp_dict["checkpoints"]:
                chk["open_time"]    = StringFromUnixTime(chk["open_time"]["$date"])
                chk["close_time"]   = StringFromUnixTime(chk["close_time"]["$date"])
            return jsonify(resp_dict)
        except:
            return Response(dumps({"Message": f"Object w/ oid {str(id)} not found in database!"}), mimetype="application/json", status=404)
    def delete(self, id):
        # Fairly self-explanatory
        try:
            Brevet.objects.get(id=str(id)).delete()
            return Response(dumps({"Message": f"Object w/ oid {str(id)} successfully deleted!"}), mimetype="application/json", status=200)
        except:
            return Response(dumps({"Message": f"Object w/ oid {str(id)} not found in database!"}), mimetype="application/json", status=404)
    def put(self, id):
        try:
            # This operates almost exactly like Brevets' (plural)'s POST method.
            vals = list(request.get_json(force=True).values())

            # Only accept 102 values. Two Brevet values, 5 * 20 = 100 checkpoint values.
            if(len(vals) == 102):

                embedded_checkpoints = []
                for i in range(20):
                    chkpt = Checkpoint(
                        distance = 0,
                        location = "%NULL%",
                        open_time=datetime.strptime("1/1/1970 00:00:00", "%m/%d/%Y %H:%M:%S"),
                        close_time=datetime.strptime("1/1/1970 00:00:00", "%m/%d/%Y %H:%M:%S")
                    )
                    if len(vals[3 + i * 5]):
                        chkpt.distance = float(vals[3 + i * 5])
                        chkpt.location = vals[4 + i * 5]
                        chkpt.open_time = datetime.strptime(vals[5 + i * 5], "%Y-%m-%dT%H:%M")
                        chkpt.close_time = datetime.strptime(vals[6 + i * 5], "%Y-%m-%dT%H:%M")
                    embedded_checkpoints.append(chkpt)

                Brevet.objects(id=str(id)).update_one(
                    set__length=float(vals[0]),
                    set__start_time=datetime.strptime(vals[1], "%Y-%m-%dT%H:%M"),
                    set__checkpoints=embedded_checkpoints
                )
                return Response(dumps({"Message": f"Object w/ oid {str(id)} successfully updated!"}), mimetype="application/json", status=200)
            else:
                return Response(dumps({"Message": f"Expected exactly 102 key-value pairs in PUT data. Please verify."}), mimetype="application/json", status=400)
        
        except:
            return Response(dumps({"Message": f"Object w/ oid {str(id)} not found in database, or PUT data was invalid!"}), mimetype="application/json", status=404)
        