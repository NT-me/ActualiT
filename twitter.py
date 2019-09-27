from tweetscrape.profile_tweets import TweetScrapperProfile as ts
import utils as u
from threading import Thread
from queue import Queue

PATH_FileRes = "tweetRES.json"


class TwitterWork(Thread):
	def __init__(self, queueIn, queueOut):
		Thread.__init__(self)
		self.queueIn = queueIn
		self.queueOut = queueOut

	def run(self):
		item = self.queueIn.get()
		res = ts(item, 10, PATH_FileRes, "json")
		self.queueOut.put(res)
		self.queueIn.task_done()


def askTwitter():
	print("--=Start twitter=--")
	liste = u.TxtToList(open('twitter_list.txt'))
	thread_count = len(liste)
	queueIn = Queue()
	queueOut = Queue()

	for i in range(thread_count):
		TW = TwitterWork(queueIn, queueOut)
		TW.deamon = True
		TW.start()

	for compte in liste:
		queueIn.put(compte)
	queueIn.join()

	while queueOut.empty() == False:
		res = queueOut.get()
		res.get_profile_tweets()
	queueOut.task_done()

	print("--=End twitter=--")
