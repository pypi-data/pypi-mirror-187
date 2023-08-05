"""Test cases for the green energy api module"""
from unittest import mock
import pytest

from green_energy_api.green_energy_api import GreenEnergyApi

ENERGY_PRICE_RESPONSE_DE = {
    "object": "list",
    "data": [
        {
            "start_timestamp": 1673942400000,
            "end_timestamp": 1673946000000,
            "marketprice": 136.1,
            "unit": "Eur/MWh"
        },
        {
            "start_timestamp": 1673946000000,
            "end_timestamp": 1673949600000,
            "marketprice": 126.17,
            "unit": "Eur/MWh"
        },
        {
            "start_timestamp": 1673949600000,
            "end_timestamp": 1673953200000,
            "marketprice": 122.75,
            "unit": "Eur/MWh"
        },
    ],
}


ENERGY_DATA_API_URL = "https://api.awattar.de"


# pylint: disable=unused-argument
def mocked_requests_get(*args, **kwargs):
    """Module handling mocked API requests"""

    # pylint: disable=too-few-public-methods
    class MockResponse:
        """Class handling mocked API responses"""

        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            """Return data as a JSON"""
            return self.json_data

    if args[0] == f"{ENERGY_DATA_API_URL}/v1/marketdata":
        return MockResponse(ENERGY_PRICE_RESPONSE_DE, 200)

    return MockResponse(None, 404)


@mock.patch(
    "requests.get",
    mock.Mock(side_effect=mocked_requests_get),
)
def test_get_co2_forecast() -> None:
    """Test if the forecast data is returned"""
    api = GreenEnergyApi(ENERGY_DATA_API_URL)
    assert api.get_electricity_price() == ENERGY_PRICE_RESPONSE_DE


@mock.patch(
    "requests.get",
    mock.Mock(side_effect=mocked_requests_get),
)
def test_request_status_error() -> None:
    """Test if API call fails"""
    api = GreenEnergyApi("http://localhost:3001")
    with pytest.raises(Exception) as exception:
        api.get_electricity_price()
    assert str(exception.value) == "Request failed with: None"
