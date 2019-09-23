from twitter_scraper import tweets as ts
import json
import utils as u
from threading import Thread
from queue import Queue
import random as r

PATH_FileRes = "tweetRES.json"


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


class TwitterWork(Thread):
	def __init__(self, queue):
		Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			res = dict()
			inc = r.randint(0, 1000000)
			print(inc)
			item = self.queue.get()
			parse = ts.get_tweets(item, pages=1)
			print(item)
			for tweet in parse:
				res[inc] = tweet
				res[inc]["time"] = u.convert_time(res[inc]["time"])
				res[inc]["from"] = "twitter"
				res[inc]["author"] = item

				inc = inc + 1

			return res
			self.queue.task_done()


def askTwitter():
	print("--=Start twitter=--")
	liste = TxtToList(open('twitter_list.txt'))
	thread_count = len(liste)

	queue = Queue()

	for i in range(thread_count):
		TW = TwitterWork(queue)
		TW.deamon = True
		TW.start()

	for compte in liste:
		queue.put(compte)

	with open(PATH_FileRes, 'w') as f:
		f.write(json.dumps(res, indent=4))
	queue.join()
	print("--=End twitter=--")
