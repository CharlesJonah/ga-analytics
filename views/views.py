from flask_restful import Resource

from helpers import client
from queries import GET_ALL_SESSIONS, SESSIONS_PER_USER, TIME_TO_ORDER_CONFIRMATION


class TotalSessions(Resource):
    def get(self):
        """Endpoint is supposed to return total number of sessions"""

        query_job = client.query(GET_ALL_SESSIONS)  # API request

        results = [result for result in list(query_job.result())]

        return {"total_sessions": results[0][0]}


class SessionsPerUser(Resource):
    def get(self):
        """Endpoint is supposed to return total number of sessions per user"""

        query_job = client.query(SESSIONS_PER_USER)  # API request

        results = [
            {"fullvisitorid": result[0], "maxVisitNumber": result[1]}
            for result in list(query_job.result())
        ]

        return {"sessions_per_user": results}


class TimeToOrderConfirmation(Resource):
    def get(self):
        """Endpoint is supposed to return time taken to get to order confirmation screen per session"""

        query_job = client.query(TIME_TO_ORDER_CONFIRMATION)  # API request

        results = [result for result in list(query_job.result())]

        milliseconds_to_mins = float((results[0][0] / float(1000 * 60))) % 60

        return {"time_to_order_confirmation": f"{milliseconds_to_mins} mins"}
