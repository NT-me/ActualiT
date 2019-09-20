import json
import newsAPI as napi
from tinydb import TinyDB, Query
import os
import feed
import reddit
import twitter
import re
import utils as u

def parse(nom_file):
	#Parse du fichier et transormation en dico
	File = open(nom_file,"r")
	article = json.loads(File.read())
	File.close()
	os.remove(nom_file)

	return article

def withoutHTML(string):
	string = re.sub("<[^>]+>","",string)

	return string
def all_ask():
	#Fichie de sortie
	PATH_OutFile = "mainCol.json"
	db = TinyDB(PATH_OutFile)

	print("--=Start ask=--")

	print("--=Start NAC=--")
	#Ask newsAPI
	napi.askNAC()
	print("--=End NAC=--")

	print("--=Start feed=--")
	#Ask feed
	feed.askFeeds()
	print("--=End feed=--")

	print("--=Start reddit=--")
	#Ask reddit
	reddit.askReddit()
	print("--=End reddit=--")

	print("--=Start twitter=--")
	#Ask twitter
	twitter.askTwitter()
	print("--=End twitter=--")

	print("--=End ask=--")


def all_parse():

	# Fichier de sortie
	PATH_OutFile = u.PATH_DB
	db = TinyDB(PATH_OutFile)
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
	# Forme d'un article dans la DB article
	# ID
	# Titre
	# Auteur
	# info_source
	# Lien
	# Resumé
	# Lien image
	# Date de publication

	titre = None
	auteur = None
	info_source = None
	lien = None
	resume = None
	lien_img = None
	date = None
	module_source = None

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
		if db.search(Query().Titre == titre) == []:
			ID = hash(titre)
			db.insert({"ID":ID, "Titre": titre, "Auteur": auteur, "info_source": info_source,
			"Lien": lien, "Contenu": resume, "URL_image": lien_img, "Publication": date, "module_source": module_source})
	print("===- News Api OK -===")

	print("===- Feed START -===")
	for i in articleFEED:
		for item in articleFEED[i]:
			titre = item["title"]
			try :
				auteur = item["author"]
			except:
				auteur = None
				print("F Pas d'auteur trouvé")
			info_source = item["source"]
			lien = item["link"]
			resume = item["summary"]
			try :
				lien_img = item["links"][1]["href"]
			except:
				lien_img = None
				print("F Pas d'image trouvée")
			date = item["published"]
			module_source = item["from"]
			if db.search(Query().Titre == titre) == []:
				ID = hash(titre)
				db.insert({"ID":ID, "Titre":titre, "Auteur":auteur, "info_source":info_source,
				"Lien": lien, "Contenu":resume, "URL_image":lien_img, "Publication": date, "module_source":module_source})
	print("===- Feed OK -===")

	print("==- Reddit START -==")
	for i in articleREDDIT:
		for item in articleREDDIT[i]:
			titre = item["title"]
			try :
				auteur = item["author"]
			except:
				auteur = None
				print("Pas d'auteur trouvé")
			info_source = item["tags"][0]["label"]
			lien = item["link"]
			resume = withoutHTML(item["summary"])
			lien_img = None
			date = u.convert_time(item["updated"])
			module_source = item["from"]
			if db.search(Query().Titre == titre) == []:
				ID = hash(titre)
				db.insert({"ID":ID, "Titre":titre, "Auteur":auteur, "info_source":info_source,
				"Lien": lien, "Contenu":resume, "URL_image":lien_img, "Publication": date, "module_source":module_source})
	print("===- Reddit OK -===")

	print("==- Twitter START -==")
	for i in articleTWEET:
		item = articleTWEET[i]
		titre = "Tweet de "+item["author"]
		try :
			titre = titre +"-"+ item["entries"]["hashtags"][0]
		except:
			print("Pas de #")
		auteur = item["author"]
		info_source = item["from"]
		lien = "https://www.twitter.com/home/"+item["tweetId"]
		resume = item["text"]
		try :
			lien_img = item["entries"]["photos"][0]
		except:
			try:
				lien_img = item["entries"]["videos"][0]
			except:
				lien_img = None
		date = item["time"]
		module_source = item["from"]
		if db.search(Query().Titre == titre) == []:
			ID = hash(titre)
			db.insert({"ID":ID, "Titre":titre, "Auteur":auteur, "info_source":info_source,
			"Lien": lien, "Contenu":resume, "URL_image":lien_img, "Publication": date, "module_source":module_source})
	print("===- Twitter OK -===")


def gen_mainCol():
	all_ask()
	all_parse()
	return 0
