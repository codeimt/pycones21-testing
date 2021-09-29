import datetime
from freezegun import freeze_time
from datetime import timedelta


def day_tomorrow(today):
    return today + timedelta(days=1)


def test_day_injection():
    today = datetime.datetime(2021, 10, 2)
    tomorrow = day_tomorrow(today)

    assert tomorrow == 3


@freeze_time("2021-10-02")
def test_date_naive():
    today = datetime.datetime.today()
    tomorrow = day_tomorrow(today)

    assert tomorrow == 3
