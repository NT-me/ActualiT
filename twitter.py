from tweetscrape.profile_tweets import TweetScrapperProfile as ts
import utils as u
from threading import Thread
from queue import Queue

PATH_FileRes = "tweetRES.json"


class TwitterWork(Thread):
	def __init__(self, queueIn):
		Thread.__init__(self)
		self.queueIn = queueIn

	def run(self):
			item = self.queueIn.get()
			res = ts(item, 40, PATH_FileRes, "json")
			res.get_profile_tweets()
			self.queueIn.task_done()


@u.MTime
def askTwitter():
	print("--=Start twitter=--")
	liste = u.TxtToList(open('twitter_list.txt'))
	thread_count = len(liste)
	queueIn = Queue()

	for i in range(thread_count):
		TW = TwitterWork(queueIn)
		TW.deamon = True
		TW.start()

	for compte in liste:
		queueIn.put(compte)

	queueIn.join()
	print("--=End twitter=--")
