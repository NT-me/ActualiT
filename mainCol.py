import json
import newsAPI as napi
from tinydb import TinyDB, Query
import os
import feed
import reddit
import twitter
import re

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

#Fichier de source de newsAPI
PATH_FileNA = napi.PATH_FileRes

#Fichier de source de feed
PATH_FileFEED = feed.PATH_FileRes

#Fichier de source de reddit
PATH_FileREDDIT = reddit.PATH_FileRes

#Fichie de sortie
PATH_OutFile = "mainCol.json"
db = TinyDB(PATH_OutFile)

#Ask newsAPI
napi.askNAC()

#Ask feed
feed.askFeeds()

#Ask reddit
reddit.askReddit()

# Parse les fichiers sources
articleNA=parse(PATH_FileNA)
articleFEED=parse(PATH_FileFEED)
articleREDDIT=parse(PATH_FileREDDIT)

#Forme d'un article dans la DB article
# ID
# Titre
# Auteur
# Nom du journal
# Lien
# Resumé
# Lien image
# Date de publication

titre = None
auteur = None
nom_Du_Journal = None
lien = None
resume = None
lien_img = None
date = None
source = None

print("===- News API START -===")
for item in articleNA["articles"]:
	titre = item["title"]
	auteur = item["author"]
	nom_Du_Journal = item["source"]["name"]
	lien = item["url"]
	resume = item["content"]
	lien_img = item["urlToImage"]
	date = item["publishedAt"]
	source = item["from"]
	if db.search(Query().Titre == titre) == []:
		ID = hash(titre)
		db.insert({"ID":ID, "Titre":titre, "Auteur":auteur, "Nom du journal":nom_Du_Journal,
		"Lien": lien, "Contenu":resume, "URL_image":lien_img, "Publication": date, "source":source})
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
		nom_Du_Journal = item["from"]
		lien = item["link"]
		resume = item["summary"]
		try :
			lien_img = item["links"][1]["href"]
		except:
			lien_img = None
			print("F Pas d'image trouvée")
		date = item["published"]
		source = item["from"]
		if db.search(Query().Titre == titre) == []:
			ID = hash(titre)
			db.insert({"ID":ID, "Titre":titre, "Auteur":auteur, "Nom du journal":nom_Du_Journal,
			"Lien": lien, "Contenu":resume, "URL_image":lien_img, "Publication": date, "source":source})
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
		nom_Du_Journal = item["tags"][0]["label"]
		lien = item["link"]
		resume = withoutHTML(item["summary"])
		lien_img = None
		date = item["updated"]
		source = item["from"]
		if db.search(Query().Titre == titre) == []:
			ID = hash(titre)
			db.insert({"ID":ID, "Titre":titre, "Auteur":auteur, "Nom du journal":nom_Du_Journal,
			"Lien": lien, "Contenu":resume, "URL_image":lien_img, "Publication": date, "source":source})
print("===- Reddit OK -===")
