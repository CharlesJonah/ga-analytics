from queries import (
    GET_ALL_SESSIONS,
    SESSIONS_PER_USER,
    TIME_TO_ORDER_CONFIRMATION,
    CALCULATE_COORDINATES_CHANGE,
    ORDER_PLACED_IF_CUSTOMER_CHANGED_LOCATION,
    ORDER_PLACED_PER_VISITOR_ID,
)

from helpers import client


class TotalSessionsBusinessLogic:
    @staticmethod
    def get_total_sessions_from_bq(query):
        query_job = client.query(query)  # API request
        return list(query_job.result())

    @staticmethod
    def process_total_sessions_data(results):
        results = [result for result in results]
        return results[0][0]


class SessionsPerUserBusinessLogic:
    @staticmethod
    def get_sessions_per_user_from_bq(query):
        query_job = client.query(query)  # API request
        return list(query_job.result())

    @staticmethod
    def process_sessions_per_user_data(results):
        return [
            {"fullvisitorid": result[0], "maxVisitNumber": result[1]}
            for result in results
        ]


class TimeToOrderConfirmationBusinessLogic:
    @staticmethod
    def get_time_to_order_confirmation_from_bq(query):
        query_job = client.query(query)  # API request
        return [result for result in list(query_job.result())]

    @staticmethod
    def process_time_to_order_confirmation_data(results):
        milliseconds_to_mins = float((results[0][0] / float(1000 * 60))) % 60
        return f"{milliseconds_to_mins} mins"


class GetCoordinatesChangeBusinessLogic:
    @staticmethod
    def get_coordinates_change_from_bq(query):
        query_job = client.query(query)  # API request
        return [result for result in list(query_job.result())]

    @staticmethod
    def process_coordinates_change_data(results):
        return [
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
            for result in results
        ]


class OrdersPlacedWithCoordinatesChangeBusinessLogic:
    @staticmethod
    def get_orders_placed_with_coordinates_change(query):
        query_job = client.query(query)  # API request
        return [result for result in list(query_job.result())]

    @staticmethod
    def process_orders_placed_with_coordinates_change_data(results):
        return [
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
            for result in results
        ]


class GetOrderDetailsPerFullVisitorIdBusinessLogic:
    @staticmethod
    def get_order_details_per_full_visitor_id(query):
        query_job = client.query(query)  # API request
        return [result for result in list(query_job.result())]

    @staticmethod
    def process_order_details_per_full_visitor_id_data(results):
        return [
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
            for result in results
        ]
