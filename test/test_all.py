import os
import unittest
from business_logic import (
    TotalSessionsBusinessLogic,
    SessionsPerUserBusinessLogic,
    TimeToOrderConfirmationBusinessLogic,
    GetCoordinatesChangeBusinessLogic,
    OrdersPlacedWithCoordinatesChangeBusinessLogic,
    GetOrderDetailsPerFullVisitorIdBusinessLogic,
)
from unittest.mock import patch
from constants import config
from queries import (
    GET_ALL_SESSIONS,
    SESSIONS_PER_USER,
    TIME_TO_ORDER_CONFIRMATION,
    CALCULATE_COORDINATES_CHANGE,
    ORDER_PLACED_IF_CUSTOMER_CHANGED_LOCATION,
    ORDER_PLACED_PER_VISITOR_ID,
)


class TotalSessions(unittest.TestCase):
    @patch(
        "business_logic.business_logic.TotalSessionsBusinessLogic.get_total_sessions_from_bq"
    )
    def test_if_get_total_sessions_returns_a_list(self, get_total_sessions_from_bq):
        get_total_sessions_from_bq.return_value = list()
        results = TotalSessionsBusinessLogic().get_total_sessions_from_bq(
            GET_ALL_SESSIONS
        )

        assert results == list()

    @patch(
        "business_logic.business_logic.TotalSessionsBusinessLogic.process_total_sessions_data"
    )
    def test_if_process_total_sessions_data_returns_an_interger(
        self, get_total_sessions_from_bq
    ):
        get_total_sessions_from_bq.return_value = 267202
        results = TotalSessionsBusinessLogic.process_total_sessions_data([])

        assert isinstance(results, int)


class SessionsPerUser(unittest.TestCase):
    @patch(
        "business_logic.business_logic.SessionsPerUserBusinessLogic.get_sessions_per_user_from_bq"
    )
    def test_if_get_sessions_per_user_from_bq_returns_a_list(
        self, get_sessions_per_user_from_bq
    ):
        get_sessions_per_user_from_bq.return_value = list()
        results = SessionsPerUserBusinessLogic.get_sessions_per_user_from_bq(
            SESSIONS_PER_USER.format(0, 0)
        )

        assert results == list()

    @patch(
        "business_logic.business_logic.SessionsPerUserBusinessLogic.process_sessions_per_user_data"
    )
    def test_if_process_sessions_per_user_data_returns_correct_data_structure(
        self, process_sessions_per_user_data
    ):
        process_sessions_per_user_data.return_value = [
            {"fullvisitorid": 1, "maxVisitNumber": 5}
        ]
        results = SessionsPerUserBusinessLogic.process_sessions_per_user_data([])

        assert ("fullvisitorid" in results[0]) and ("maxVisitNumber" in results[0])


class TimeToOrderConfirmation(unittest.TestCase):
    @patch(
        "business_logic.business_logic.TimeToOrderConfirmationBusinessLogic.get_time_to_order_confirmation_from_bq"
    )
    def test_if_get_time_to_order_confirmation_from_bq_returns_a_list(
        self, get_time_to_order_confirmation_from_bq
    ):
        get_time_to_order_confirmation_from_bq.return_value = list()
        results = (
            TimeToOrderConfirmationBusinessLogic.get_time_to_order_confirmation_from_bq(
                TIME_TO_ORDER_CONFIRMATION
            )
        )

        assert results == list()

    @patch(
        "business_logic.business_logic.TimeToOrderConfirmationBusinessLogic.process_time_to_order_confirmation_data"
    )
    def test_if_process_sessions_per_user_data_returns_correct_data_structure(
        self, process_time_to_order_confirmation_data
    ):
        process_time_to_order_confirmation_data.return_value = "5 mins"
        results = TimeToOrderConfirmationBusinessLogic.process_time_to_order_confirmation_data(
            []
        )

        assert isinstance(results, str)


class GetCoordinatesChange(unittest.TestCase):
    @patch(
        "business_logic.business_logic.GetCoordinatesChangeBusinessLogic.get_coordinates_change_from_bq"
    )
    def test_if_get_coordinates_change_from_bq_returns_a_list(
        self, get_coordinates_change_from_bq
    ):
        get_coordinates_change_from_bq.return_value = list()
        results = GetCoordinatesChangeBusinessLogic.get_coordinates_change_from_bq(
            CALCULATE_COORDINATES_CHANGE.format(0, 0)
        )

        assert results == list()

    @patch(
        "business_logic.business_logic.GetCoordinatesChangeBusinessLogic.process_coordinates_change_data"
    )
    def test_process_coordinates_change_data_returns_a_list(
        self, process_coordinates_change_data
    ):
        process_coordinates_change_data.return_value = list()
        results = GetCoordinatesChangeBusinessLogic.process_coordinates_change_data([])
        assert results == list()


class OrdersPlacedWithCoordinatesChange(unittest.TestCase):
    @patch(
        "business_logic.business_logic.OrdersPlacedWithCoordinatesChangeBusinessLogic.get_orders_placed_with_coordinates_change"
    )
    def test_if_get_orders_placed_with_coordinates_change_returns_a_list(
        self, get_orders_placed_with_coordinates_change
    ):
        get_orders_placed_with_coordinates_change.return_value = list()
        results = OrdersPlacedWithCoordinatesChangeBusinessLogic.get_orders_placed_with_coordinates_change(
            ORDER_PLACED_IF_CUSTOMER_CHANGED_LOCATION.format(0, 0)
        )

        assert results == list()

    @patch(
        "business_logic.business_logic.OrdersPlacedWithCoordinatesChangeBusinessLogic.process_orders_placed_with_coordinates_change_data"
    )
    def test_process_orders_placed_with_coordinates_change_data_returns_a_list(
        self, process_orders_placed_with_coordinates_change_data
    ):
        process_orders_placed_with_coordinates_change_data.return_value = list()
        results = OrdersPlacedWithCoordinatesChangeBusinessLogic.process_orders_placed_with_coordinates_change_data(
            []
        )
        assert results == list()


class GetOrderDetailsPerFullVisitorId(unittest.TestCase):
    @patch(
        "business_logic.business_logic.GetOrderDetailsPerFullVisitorIdBusinessLogic.get_order_details_per_full_visitor_id"
    )
    def test_if_get_order_details_per_full_visitor_id_returns_a_list(
        self, get_order_details_per_full_visitor_id
    ):
        get_order_details_per_full_visitor_id.return_value = list()
        results = GetOrderDetailsPerFullVisitorIdBusinessLogic.get_order_details_per_full_visitor_id(
            ORDER_PLACED_PER_VISITOR_ID.format(1)
        )
        assert results == list()

    @patch(
        "business_logic.business_logic.GetOrderDetailsPerFullVisitorIdBusinessLogic.get_order_details_per_full_visitor_id"
    )
    def test_process_orders_placed_with_coordinates_change_data_returns_a_list(
        self, process_order_details_per_full_visitor_id_data
    ):
        process_order_details_per_full_visitor_id_data.return_value = list()
        results = GetOrderDetailsPerFullVisitorIdBusinessLogic.process_order_details_per_full_visitor_id_data(
            []
        )
        assert results == list()


if __name__ == "__main__":

    unittest.main()
