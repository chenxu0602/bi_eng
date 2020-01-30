from flask import Flask, jsonify, abort, request
from flask_restful import reqparse, Api, Resource
from collections import defaultdict
from math import sin, cos, sqrt, atan2, radians
from threading import Lock

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("origin", type=float, required=True, action="append")
parser.add_argument("destination", type=float, required=True, action="append")
parser.add_argument("take_oid", type=int)

orders = defaultdict(dict)

def get_paginated_list(results, url, page, limit):
    try:
        page, limit = int(page), int(limit)
    except:
        return  {"error": "ERROR_DESCRIPTION"}

    if page >= 1 and limit > 0:
        total_records = len(results)
        total_pages = (total_records - 1) // limit + 1
        if not (1 <= page <= total_pages): abort(404)
        return results[(page - 1)*limit:min(page*limit, total_records)]
    else:
        return  {"error": "ERROR_DESCRIPTION"}



R = 6373.0

def calc_dist(org, des):
    try:
        lat1, lon1 = float(org[0]), float(org[1])
        lat2, lon2 = float(des[0]), float(des[1])
    except:
        return -1

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return int(R * c)

class HandleOrders(Resource):
    def get(self):
        if orders and len(orders) > 0:
            return jsonify(get_paginated_list(
                list(orders.values()),
                "/orders",
                page=request.args.get('page', 1),
                limit=request.args.get('limit', 2000)))
        else:
            return {"error": "ERROR_DESCRIPTION"}

    def delete(self, oid):
        del orders[oid]
        return "delete success", 204

    def post(self):
        oid = len(orders) + 1

        args = parser.parse_args()
        origin = args["origin"]
        destination = args["destination"]

        dist = None
        try:
            dist = calc_dist(origin, destination)
        except:
            return {"error": "ERROR_DESCRIPTION"}

        if dist and dist >= 0:
            order = {
                "id": oid,
                "distance": dist,
                "status": "UNASSIGNED"
            }

            orders[oid] = order
            return orders[oid], 201

        return {"error": "ERROR_DESCRIPTION"}, 404


class TakeOrders(Resource):
    def __init__(self):
        self.lock = Lock()

    def patch(self, oid):
        with self.lock:
            if oid in orders and orders[oid]["status"] == "UNASSIGNED":
                orders[oid]["status"] = "SUCCESS"
                return {"status": "SUCCESS"}, 201
            else:
                return {"error": "ERROR_DESCRIPTION"}, 404

    def get(self, oid):
        if oid in orders:
            return orders[oid], 201
        else:
            return {"error": "ERROR_DESCRIPTION"}, 404


api.add_resource(HandleOrders, "/orders", endpoint="orders")
api.add_resource(TakeOrders, "/orders/<int:oid>", endpoint="order")

if __name__ == "__main__":
    app.run(debug=True, port=8080)