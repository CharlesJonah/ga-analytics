from flask_restful import Resource, request

from helpers import client
from queries import (
    GET_ALL_SESSIONS,
    SESSIONS_PER_USER,
    TIME_TO_ORDER_CONFIRMATION,
    CALCULATE_COORDINATES_CHANGE,
    ORDER_PLACED_IF_CUSTOMER_CHANGED_LOCATION,
    ORDER_PLACED_PER_VISITOR_ID,
)


class TotalSessions(Resource):
    def get(self):
        """Endpoint is supposed to return total number of sessions"""

        query_job = client.query(GET_ALL_SESSIONS)  # API request

        results = [result for result in list(query_job.result())]

        return {"totalSessions": results[0][0]}, 200


class SessionsPerUser(Resource):
    def get(self):
        """Endpoint is supposed to return total number of sessions per user"""

        args = request.args
        if ("limit" in args) and ("offset" in args):
            query_job = client.query(
                SESSIONS_PER_USER.format(args["limit"], args["offset"])
            )  # API request
        else:
            return {"results", "please provide both limit and offset"}, 400

        results = [
            {"fullvisitorid": result[0], "maxVisitNumber": result[1]}
            for result in list(query_job.result())
        ]

        return {"sessionsPerUser": results}, 200


class TimeToOrderConfirmation(Resource):
    def get(self):
        """Endpoint is supposed to return time taken to get to order confirmation screen per session"""

        query_job = client.query(TIME_TO_ORDER_CONFIRMATION)  # API request

        results = [result for result in list(query_job.result())]

        milliseconds_to_mins = float((results[0][0] / float(1000 * 60))) % 60

        return {"timeToOrderConfirmation": f"{milliseconds_to_mins} mins"}, 200


class GetCoordinatesChange(Resource):
    def get(self):
        """
        Endpoint is supposed to return coordinates change of users between initial screens
        and ending screens in the ordering process
        """

        args = request.args
        if ("limit" in args) and ("offset" in args):
            query_job = client.query(
                CALCULATE_COORDINATES_CHANGE.format(args["limit"], args["offset"])
            )  # API request

            results = [
                {
                    "fullvisitorid": result[0],
                    "visitNumber": result[1],
                    "visitId": result[2],
                    "screenStartType": result[3],
                    "latStart": result[4],
                    "longStart": result[5],
                    "screenTypeEnd": result[6],
                    "latStart": result[7],
                    "latEnd": result[8],
                    "coordinatesChange": result[9],
                }
                for result in list(query_job.result())
            ]
            return {"results": results}, 200
        else:
            return {"results", "please provide both limit and offset"}, 400


class OrdersPlacedWithCoordinatesChange(Resource):
    def get(self):
        """
        Endpoint is supposed to return visitors who placed orders with change of their geolocations
        """

        args = request.args
        if ("limit" in args) and ("offset" in args):
            query_job = client.query(
                ORDER_PLACED_IF_CUSTOMER_CHANGED_LOCATION.format(
                    args["limit"], args["offset"]
                )
            )  # API request
            results = [
                {
                    "fullvisitorid": result[0],
                    "visitNumber": result[1],
                    "visitId": result[2],
                    "isOrderPlaced": True if result[15] else False,
                    "isOrderDelivered": True if result[21] else False,
                    "isDestinationMatched": True if result[20] == result[21] else False,
                    "geopointCustomer": result[20],
                    "geopointDropoff": result[21],
                }
                for result in list(query_job.result())
            ]
            return {"results": results}, 200
        else:
            return {"results", "please provide both limit and offset"}, 400


class GetOrderDetailsPerFullVisitorId(Resource):
    def get(self):
        """
        Endpoint is supposed to return details of an order and full visitor per full visitor id
        """

        args = request.args
        if "fullVisitorId" in args:
            query_job = client.query(
                ORDER_PLACED_PER_VISITOR_ID.format(args["fullVisitorId"])
            )  # API request
            results = [
                {
                    "fullvisitorid": result[0],
                    "visitNumber": result[1],
                    "visitId": result[2],
                    "address_changed": True
                    if f"{result[11]},{result[12]}" != f"{result[13]},{result[14]}"
                    else False,
                    "is_order_placed": True if result[20] else False,
                    "is_order_delivered": True if result[26] else False,
                    "application_type:": result[4],
                }
                for result in list(query_job.result())
            ]
            return {"results": results}, 200
        else:
            return {"results", "please provide fullVisitorId"}, 400
