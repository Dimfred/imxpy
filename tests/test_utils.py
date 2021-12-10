import pytest
from utils import SafeNumber


class TestSafeNumber:
    def test_okay_1_eth(self, one_eth):
        n = SafeNumber(1, decimals=18, as_wei=False).value
        assert len(str(n)) == 19
        assert n == str(one_eth)

        n = SafeNumber("1", decimals=18, as_wei=False).value
        assert len(str(n)) == 19
        assert n == str(one_eth)

    def test_okay_returns_wei(self, one_eth):
        n = SafeNumber(one_eth, decimals=18, as_wei=True).value
        assert n == str(one_eth)

    def test_okay_leading_zeros_removed(self, one_eth):
        n = SafeNumber("0.01", decimals=3, as_wei=False).value
        assert n == "10"

    def test_okay_with_number_before_and_after_comma(self):
        n = SafeNumber("1.02", decimals=3, as_wei=False).value
        assert n == "1020"

    def test_okay_0_5_eth(self, half_eth):
        n = SafeNumber("0.5", decimals=18, as_wei=False).value
        assert n == str(half_eth)

    def test_okay_0_eth(self):
        n = SafeNumber("0", decimals=18, as_wei=False).value
        assert n == "0"

        n = SafeNumber(0, decimals=18, as_wei=False).value
        assert n == "0"

    def test_fails_with_float(self):
        with pytest.raises(ValueError) as e:
            SafeNumber(1.0)

        assert "Only 'str' and 'int'" in str(e.value)

    def test_fails_with_comma(self):
        with pytest.raises(ValueError) as e:
            SafeNumber("1,2", as_wei=True)
        assert "invalid literal" in str(e.value)

    def test_fails_too_much_decimals(self):
        n = "0.12345"
        with pytest.raises(ValueError) as e:
            SafeNumber(n, decimals=4)
        assert "More decimals" in str(e.value)
