import xml.etree.ElementTree as ET
from unittest.mock import Mock, patch

import pytest

from src.currency import get_currencies, get_sp500


@pytest.fixture
def data() -> str:
    return """<?xml version="1.0" encoding="windows-1251"?>
<ValCurs Date="15.05.2024" name="Foreign Currency Market">
    <Valute ID="R01235">
        <NumCode>840</NumCode>
        <CharCode>USD</CharCode>
        <Nominal>1</Nominal>
        <Name>Доллар США</Name>
        <Value>74,3250</Value>
    </Valute>
    <Valute ID="R01239">
        <NumCode>978</NumCode>
        <CharCode>EUR</CharCode>
        <Nominal>1</Nominal>
        <Name>Евро</Name>
        <Value>90,1234</Value>
    </Valute>
</ValCurs>"""


def test_get_currencies_rub() -> None:
    assert get_currencies(["RUB"]) == [{"currency": "RUB", "rate": "1"}]


def test_get_currencies(data: str) -> None:
    with patch("builtins.open") as mock_open:
        with patch("xml.etree.ElementTree.parse") as parse_mock:
            mock_tree = ET.ElementTree(ET.fromstring(data))
            parse_mock.return_value = mock_tree
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.read.return_value = data
            value = get_currencies(["USD", "EUR"])
            assert value == [
                {"currency": "USD", "rate": "74.3250"},
                {"currency": "EUR", "rate": "90.1234"},
            ]


@patch("requests.get")
def test_get_sp500(mock_get: Mock) -> None:
    mock_get.return_value.json.return_value = {
        "Meta Data": {
            "3. Last Refreshed": "2024-06-27",
        },
        "Time Series (Daily)": {
            "2024-06-27": {
                "4. close": "214.1000",
            }
        },
    }
    assert get_sp500(["AAPL"]) == [{"price": "214.1000", "stock": "AAPL"}]
