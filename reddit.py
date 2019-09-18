import feedparser as fp
import json
import asyncio
import purifier 

PATH_FileRes = "redditRES.json"
def TxtToList(f):
	"""
	Permet de transformer un fichier txt en une liste python
	"""
	res = []

	ligne=f.readline()
	while ligne !="":
		ligne=ligne.replace("\n","")
		res.append(ligne)
		ligne=f.readline()
	f.close()
	return res

def askReddit():
	#Liste des feeds
	FILE_liste = open("reddit_list.txt","r")
	liste = TxtToList(FILE_liste)
	res = dict()
	inc = 0

	#Parcours la liste de source
	for item in liste:
		if item[len(item)-1]=='/':
			item=item[:len(item)-1]+".rss"
		else :
			item = item+".rss"
		parse = fp.parse(item).entries
		res[inc]=parse
		# Ajoute la provenance à chaque article
		for article in res[inc]:
			article["from"]="reddit"
		inc = inc + 1

	with open(PATH_FileRes, 'w') as f:
		f.write(json.dumps(res, indent=4))
