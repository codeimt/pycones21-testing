import datetime
from freezegun import freeze_time
from datetime import timedelta


def day_tomorrow(today):
    return today + timedelta(days=1)


def test_date_naive():
    today = datetime.datetime.today()
    day_tomorrow = day_tomorrow(today)

    assert tomorrow.day == 2
