from datetime import datetime, timedelta


class TestUtils:

    @staticmethod
    def get_date_difference(days):
        time_difference = timedelta(days=days)
        current_datetime = datetime.now()
        return current_datetime + time_difference

    @staticmethod
    def get_past_date(days: int = -7):
        return TestUtils.get_date_difference(days)

    @staticmethod
    def get_future_date(days: int = 7):
        return TestUtils.get_date_difference(days)

