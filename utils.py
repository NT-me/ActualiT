from dateutil import parser as c
from datetime import datetime as dt

PATH_DB = "mainCol.json"

def convert_time(time):
	return dt.timestamp(c.parse(str(time)))
