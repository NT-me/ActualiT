from tweetscrape.profile_tweets import TweetScrapperProfile as ts
from . import utils as u
from threading import Thread
from queue import Queue
import json
from FillmainCol import wrapperDB as wdb
import requests


PATH_FileRes = "tweetRES.json"


class TwitterWork(Thread):
	def __init__(self, queueIn, queueOut):
		Thread.__init__(self)
		self.queueIn = queueIn
		self.queueOut = queueOut

	def run(self):
		item = self.queueIn.get()
		test = requests.get('https://twitter.com/{username}'.format(username=item.link))
		if test.status_code == 404:
			res = dict()
		else:
			res = ts(item.link, 10, PATH_FileRes, "json")
		self.queueOut.put(res)
		self.queueIn.task_done()


def askTwitter():
	print("--=Start twitter=--")
	liste = wdb.readOriginSources('Twitter')
	if liste != []:
		thread_count = len(liste)
		queueIn = Queue()
		queueOut = Queue()

		for i in range(thread_count):
			TW = TwitterWork(queueIn, queueOut)
			TW.deamon = False
			TW.start()

		for compte in liste:
			queueIn.put(compte)
		queueIn.join()

		while queueOut.empty() == False:
			res = queueOut.get()
			if res != {}:
				res.get_profile_tweets()
		queueOut.task_done()
	else:
		res = dict()
		with open(PATH_FileRes, 'w') as f:
			f.write(json.dumps(res, indent=4))

	print("--=End twitter=--")
