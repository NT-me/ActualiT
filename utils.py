import ciso8601 as c
from datetime import datetime as dt

def convert_time(time):
	return dt.timestamp(c.parse_datetime(str(time)))
