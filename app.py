if __name__ == "__main__":
    # this dotenv should be loaded and called first
    # had to place it here because autoformatting of the code places
    # it below the other modules
    # meaning some modules will end up not getting env variables
    from dotenv import load_dotenv

    load_dotenv()

    from flask_restful import Api
    from views import (
        TotalSessions,
        SessionsPerUser,
        TimeToOrderConfirmation,
        GetCoordinatesChange,
        OrdersPlacedWithCoordinatesChange,
        GetOrderDetailsPerFullVisitorId,
    )

    from constants import config
    from application import application

    api = Api(application, catch_all_404s=True)

    api.add_resource(TotalSessions, "/api/v1/total-sessions")
    api.add_resource(SessionsPerUser, "/api/v1/sessions-per-user")
    api.add_resource(TimeToOrderConfirmation, "/api/v1/time-to-order-confirmation")
    api.add_resource(GetCoordinatesChange, "/api/v1/get-coordinates-change")
    api.add_resource(
        OrdersPlacedWithCoordinatesChange,
        "/api/v1/orders-placed-with-coordinates-change",
    )
    api.add_resource(
        GetOrderDetailsPerFullVisitorId,
        "/api/v1/get-order-details-per-full-visitor-id",
    )

    application.run(host="0.0.0.0", debug=True)
