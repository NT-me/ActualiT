from dateutil import parser as c
from datetime import datetime as dt

def convert_time(time):
	return dt.timestamp(c.parse(str(time)))
