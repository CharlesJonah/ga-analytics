from flask_restful import Resource, request

from helpers import client
from business_logic import (
    TotalSessionsBusinessLogic,
    SessionsPerUserBusinessLogic,
    TimeToOrderConfirmationBusinessLogic,
    GetCoordinatesChangeBusinessLogic,
    OrdersPlacedWithCoordinatesChangeBusinessLogic,
    GetOrderDetailsPerFullVisitorIdBusinessLogic,
)
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

        results = TotalSessionsBusinessLogic().get_total_sessions_from_bq(
            GET_ALL_SESSIONS
        )

        total_sessions = TotalSessionsBusinessLogic().process_total_sessions_data(
            results
        )

        return {"totalSessions": total_sessions}, 200


class SessionsPerUser(Resource):
    def get(self):
        """Endpoint is supposed to return total number of sessions per user"""

        args = request.args
        if ("limit" in args) and ("offset" in args):
            results = SessionsPerUserBusinessLogic.get_sessions_per_user_from_bq(
                SESSIONS_PER_USER.format(args["limit"], args["offset"])
            )
        else:
            return {"results", "please provide both limit and offset"}, 400

        results = SessionsPerUserBusinessLogic.process_sessions_per_user_data(results)

        return {"sessionsPerUser": results}, 200


class TimeToOrderConfirmation(Resource):
    def get(self):
        """Endpoint is supposed to return time taken to get to order confirmation screen per session"""

        results = (
            TimeToOrderConfirmationBusinessLogic.get_time_to_order_confirmation_from_bq(
                TIME_TO_ORDER_CONFIRMATION
            )
        )

        time_to_order_confirmation = TimeToOrderConfirmationBusinessLogic().process_time_to_order_confirmation_data(
            results
        )

        return {"timeToOrderConfirmation": time_to_order_confirmation}, 200


class GetCoordinatesChange(Resource):
    def get(self):
        """
        Endpoint is supposed to return coordinates change of users between initial screens
        and ending screens in the ordering process
        """

        args = request.args
        if ("limit" in args) and ("offset" in args):
            results = GetCoordinatesChangeBusinessLogic.get_coordinates_change_from_bq(
                CALCULATE_COORDINATES_CHANGE.format(args["limit"], args["offset"])
            )

            results = GetCoordinatesChangeBusinessLogic.process_coordinates_change_data(
                results
            )
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
            results = OrdersPlacedWithCoordinatesChangeBusinessLogic.get_orders_placed_with_coordinates_change(
                ORDER_PLACED_IF_CUSTOMER_CHANGED_LOCATION.format(
                    args["limit"], args["offset"]
                )
            )

            results = OrdersPlacedWithCoordinatesChangeBusinessLogic.process_orders_placed_with_coordinates_change_data(
                results
            )
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
            results = GetOrderDetailsPerFullVisitorIdBusinessLogic.get_order_details_per_full_visitor_id(
                ORDER_PLACED_PER_VISITOR_ID.format(args["fullVisitorId"])
            )

            results = GetOrderDetailsPerFullVisitorIdBusinessLogic.process_order_details_per_full_visitor_id_data(
                results
            )
            return {"results": results}, 200
        else:
            return {"results", "please provide fullVisitorId"}, 400
