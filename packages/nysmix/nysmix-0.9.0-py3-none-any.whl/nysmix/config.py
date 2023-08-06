"""general configuration
"""

from datetime import date
from datetime import date, timedelta, timezone


YEAR_START = 2015
MONTH_START = 12
DAY_START = 9
DATE_START = date(year=YEAR_START, month=MONTH_START, day=DAY_START)
FORMAT_DATE = "%Y%m%d"
TZ = timezone(timedelta(hours=-5))
