import json
from FillmainCol.scrapers import newsAPI as napi
import os
from FillmainCol.scrapers import feed
from FillmainCol.scrapers import reddit
from FillmainCol.scrapers import twitter
import re
from FillmainCol.scrapers import utils as u
from threading import Thread
from . import dbToList as dbt
from objects.article import Article
from FillmainCol import wrapperDB as wdb
from queue import Queue


def reader(nom_file):
	# Lit du fichier et transormation en dico
	article = dict()
	try:
		File = open(nom_file, "r")
		try:
			article = json.loads(File.read())
		except:
			pass
		File.close()
		os.remove(nom_file)
	except FileNotFoundError:
		print(nom_file + ' introuvable.\n')

	return article


def withoutHTML(string):
	string = re.sub("<[^>]+>", "", string)

	return string


class NACWork(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		print("--=Start NAC=--")
		napi.askNAC()
		print("--=End NAC=--")


class FeedWork(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		print("--=Start feed=--")
		feed.askFeeds()
		print("--=End feed=--")


class RedditWork(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		print("--=Start reddit=--")
		reddit.askReddit()
		print("--=End reddit=--")


class TwitterWork(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		twitter.askTwitter()


def parseNAC():
	ArtList = list()
	# Fichier de source de newsAPI
	PATH_FileNA = napi.PATH_FileRes

	# Read non-formated file
	articleNA = reader(PATH_FileNA)

	print("===- News API START -===")
	for item in articleNA["articles"]:
		titre = item["title"]
		auteur = item["author"]
		info_source = item["source"]["name"]
		lien = item["url"]
		resume = item["content"]
		lien_img = item["urlToImage"]
		date = u.convert_time(item["publishedAt"])
		module_source = item["from"]
		ArtList.append(Article(hash(titre), titre, auteur, info_source, lien, resume, lien_img, date, module_source))
	print("===- News Api OK -===")

	return ArtList


def parseFeed():
	ArtList = list()

	# Fichier de source de feed
	PATH_FileFEED = feed.PATH_FileRes

	# read non-formated file
	articleFEED = reader(PATH_FileFEED)

	print("===- Feed START -===")
	for i in articleFEED:
		for item in articleFEED[i]:
			titre = withoutHTML(item["title"])
			try:
				auteur = item["author"]
			except:
				auteur = None
			info_source = item["source"]
			lien = item["link"]
			try:
				resume = withoutHTML(item["summary"])
			except:
				resume = None
			try:
				lien_img = item["links"][1]["href"]
			except:
				lien_img = None
			date = item["published"]
			module_source = item["from"]
			ArtList.append(Article(hash(titre), titre, auteur, info_source, lien, resume, lien_img, date, module_source))
	print("===- Feed OK -===")

	return ArtList


def parseReddit():
	ArtList = list()

	# Fichier de source de reddit
	PATH_FileREDDIT = reddit.PATH_FileRes

	# Read non foramted file
	articleREDDIT = reader(PATH_FileREDDIT)

	print("==- Reddit START -==")
	for i in articleREDDIT:
		for item in articleREDDIT[i]:
			titre = item["title"]
			try:
				auteur = item["author"]
			except:
				auteur = None
			info_source = item["tags"][0]["label"]
			lien = item["link"]
			resume = withoutHTML(item["summary"])
			lien_img = None
			date = u.convert_time(item["updated"])
			module_source = item["from"]
			ArtList.append(Article(hash(titre), titre, auteur, info_source, lien, resume, lien_img, date, module_source))
	print("===- Reddit OK -===")

	return ArtList


def parseTwitter():
	ArtList = list()

	# Fichier de source de twitter
	PATH_FileTWEET = twitter.PATH_FileRes

	articleTWEET = reader(PATH_FileTWEET)

	print("==- Twitter START -==")
	for i in articleTWEET:
		item = i
		titre = "Tweet de "+item["author"]
		try:
			titre = titre + "-" + item["hashtags"][0]
		except:
			pass
		auteur = item["author"]
		info_source = item["type"]
		lien = "https://twitter.com/statuses/"+item["id"]
		resume = item["text"]
		try:
			lien_img = item["entries"]["photos"][0]
		except:
			try:
				lien_img = item["entries"]["videos"][0]
			except:
				lien_img = None
		date = int(item["time"][:10])
		module_source = "Twitter"
		ArtList.append(Article(hash(titre), titre, auteur, info_source, lien, resume, lien_img, date, module_source))
	print("===- Twitter OK -===")

	return ArtList


def all_ask():
	# Déclaration des threads
	thread_NAC = NACWork()
	thread_Feed = FeedWork()
	thread_Reddit = RedditWork()
	thread_Twitter = TwitterWork()

	print("--=Start ask=--")

	# Ask newsAPI
	thread_NAC.start()

	# Ask feed
	thread_Feed.start()

	# Ask reddit
	thread_Reddit.start()

	# Ask twitter
	thread_Twitter.start()

	thread_NAC.join()
	thread_Feed.join()
	thread_Reddit.join()
	thread_Twitter.join()
	print("--=End ask=--")


class parseNAC_T(Thread):
	def __init__(self, queueOut):
		Thread.__init__(self)
		self.queueOut = queueOut

	def run(self):
		self.queueOut.put(parseNAC())


class parseFeed_T(Thread):
	def __init__(self, queueOut):
		Thread.__init__(self)
		self.queueOut = queueOut

	def run(self):
		self.queueOut.put(parseFeed())


class parseReddit_T(Thread):
	def __init__(self, queueOut):
		Thread.__init__(self)
		self.queueOut = queueOut

	def run(self):
		self.queueOut.put(parseReddit())


class parseTwitter_T(Thread):
	def __init__(self, queueOut):
		Thread.__init__(self)
		self.queueOut = queueOut

	def run(self):
		self.queueOut.put(parseTwitter())


class fillDbArt_T(Thread):
	def __init__(self, queueIn):
		super(fillDbArt_T, self).__init__()
		self.queueIn = queueIn

	def run(self):
		list = self.queueIn.get()
		wdb.insertArticles(list)


def all_parse():
	queueOut = Queue()

	NAC_T = parseNAC_T(queueOut)
	Feed_T = parseFeed_T(queueOut)
	Reddit_T = parseReddit_T(queueOut)
	Twitter_T = parseTwitter_T(queueOut)

	NAC_T.start()
	Feed_T.start()
	Reddit_T.start()
	Twitter_T.start()

	ArtList = list()

	NAC_T.join()
	Feed_T.join()
	Reddit_T.join()
	Twitter_T.join()

	while queueOut.empty() is False:
		ArtList = ArtList + queueOut.get()

	print(len(ArtList))

	queueIn = Queue()
	ArtList = wdb.deleteArticlesTooOld(ArtList, 604800)
	queueIn.put(ArtList)
	Fdb = fillDbArt_T(queueIn)
	# Fdb.daemon = True
	Fdb.start()

	return ArtList


@u.MTime
def gen_mainCol():
	all_ask()
	res = all_parse()
	wdb.globalArtList = res
	return res

	#return wdb.readAllArticles()
