"""
Main class of the package
"""
from src.py_utah_deq.data_sources.utah_deq_api import UtahDEQAPI
from src.py_utah_deq.aqi.aqi_metric import AQIMetric


class UtahDEQ:
    """
    Main class of project for retrieving AQI data.
    """
    def __init__(self, feed_id: str = "nr"):
        self.__deq_api = UtahDEQAPI(feed_id)

    def get_latest_aqi(self) -> AQIMetric:
        """
        Get the most recent AQI data for the given feed id.

        :return:
        :rtype: AQIMetric
        """
        return self.__deq_api.get_current_aqi()

    def get_deq_feed_id(self) -> str:
        """
        Returns the current feed id.

        :return:
        :rtype: str
        """
        return self.__deq_api.feed_id
