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
from FillmainCol.scrapers.utils import Article
from FillmainCol import wrapperDB as wdb


def parse(nom_file):
	# Parse du fichier et transormation en dico
	File = open(nom_file, "r")
	article = dict()
	try:
		article = json.loads(File.read())
	except:
		pass
	File.close()
	os.remove(nom_file)

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


def all_parse():

	# Fichier de source de newsAPI
	PATH_FileNA = napi.PATH_FileRes

	# Fichier de source de feed
	PATH_FileFEED = feed.PATH_FileRes

	# Fichier de source de reddit
	PATH_FileREDDIT = reddit.PATH_FileRes

	# Fichier de source de twitter
	PATH_FileTWEET = twitter.PATH_FileRes

	# Parse les fichiers sources
	articleNA = parse(PATH_FileNA)

	articleFEED = parse(PATH_FileFEED)

	articleREDDIT = parse(PATH_FileREDDIT)

	articleTWEET = parse(PATH_FileTWEET)

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
		wdb.insertArticle(Article(hash(titre), titre, auteur, info_source, lien, resume, lien_img, date, module_source))
	print("===- News Api OK -===")

	print("===- Feed START -===")
	for i in articleFEED:
		for item in articleFEED[i]:
			titre = item["title"]
			try:
				auteur = item["author"]
			except:
				auteur = None
			info_source = item["source"]
			lien = item["link"]
			resume = item["summary"]
			try:
				lien_img = item["links"][1]["href"]
			except:
				lien_img = None
			date = item["published"]
			module_source = item["from"]
			wdb.insertArticle(Article(hash(titre), titre, auteur, info_source, lien, resume, lien_img, date, module_source))
	print("===- Feed OK -===")

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
			wdb.insertArticle(Article(hash(titre), titre, auteur, info_source, lien, resume, lien_img, date, module_source))
	print("===- Reddit OK -===")

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
		lien = "https://www.twitter.com/home/"+item["id"]
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
		wdb.insertArticle(Article(hash(titre), titre, auteur, info_source, lien, resume, lien_img, date, module_source))
	print("===- Twitter OK -===")


def gen_mainCol():
	all_ask()
	all_parse()
	return dbt.sortMainCol()
