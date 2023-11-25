"""
Resource: Brevets
"""
from flask import Response, request, jsonify
from flask_restful import Resource
from datetime import datetime
from json import dumps, loads

# You need to implement this in database/models.py
from database.models import *

def StringFromUnixTime(timestamp: str) -> str:
    return datetime.utcfromtimestamp(float(timestamp)/1000).strftime("%Y-%m-%dT%H:%M")

class Brevets_Resource(Resource):
    def post(self):
        vals = list(request.get_json(force=True).values())
        if(len(vals) == 102):
            embedded_checkpoints=[]
            for i in range(20):
                chkpt = Checkpoint(
                    distance=0,
                    location= "%NULL%",
                    open_time=datetime.strptime("1/1/1970 00:00:00", "%m/%d/%Y %H:%M:%S"),
                    close_time=datetime.strptime("1/1/1970 00:00:00", "%m/%d/%Y %H:%M:%S")
                )
                if len(vals[3 + i * 5]):
                    chkpt.distance = float(vals[3 + i * 5])
                    chkpt.location = vals[4 + i * 5]
                    chkpt.open_time = datetime.strptime(vals[5 + i * 5], "%Y-%m-%dT%H:%M")
                    chkpt.close_time = datetime.strptime(vals[6 + i * 5], "%Y-%m-%dT%H:%M")
                embedded_checkpoints.append(chkpt)

            new_brev = Brevet(
                length=float(vals[0]), # 2021-01-01T00:00
                start_time=datetime.strptime(vals[1], "%Y-%m-%dT%H:%M"),
                checkpoints=embedded_checkpoints
            )
            new_brev.save()
            return Response(dumps({"Message": f"Brevet w/ oid {str(new_brev.id)} successfully created!"}), mimetype="application/json", status=200)
        else:
            return Response(dumps({"Message": f"Expected exactly 102 key-value pairs in POST data. Please verify."}), mimetype="application/json", status=400)
    def get(self):
        resp_dict = loads(Brevet.objects.to_json())
        for brev in resp_dict:
            brev["start_time"] = StringFromUnixTime(brev["start_time"]["$date"])
            for chk in brev["checkpoints"]:
                chk["open_time"]    = StringFromUnixTime(chk["open_time"]["$date"])
                chk["close_time"]   = StringFromUnixTime(chk["close_time"]["$date"])
        return jsonify(resp_dict)