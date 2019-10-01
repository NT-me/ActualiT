from dateutil import parser as c
from datetime import datetime as dt
from time import process_time


PATH_DB = "mainCol.json"


def MTime(func):
	def wrapper(*args, **kwargs):
		t = process_time()
		response = func(*args, **kwargs)
		elapsed_time = process_time() - t
		print(elapsed_time)
		return response
	return wrapper


def TxtToList(f):
	"""
	Permet de transformer un fichier txt en une liste python
	"""
	res = []

	ligne = f.readline()
	while ligne != "":
		ligne = ligne.replace("\n", "")
		res.append(ligne)
		ligne = f.readline()
	f.close()

	return res


def convert_time(time):
	return dt.timestamp(c.parse(str(time)))