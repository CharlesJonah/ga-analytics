from flask_restful import Resource


class TotalSessions(Resource):
    def get(self):
        """Endpoint is supposed to return total number of sessions"""

        return {"greeting": "Hello"}


class SessionsPerUser(Resource):
    def get(self):
        """Endpoint is supposed to return total number of sessions per user"""

        pass
