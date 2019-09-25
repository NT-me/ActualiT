import feedparser as fp
import json
import asyncio
import purifier
import utils as u

PATH_FileRes = "redditRES.json"

def askReddit():
	#Liste des feeds
	FILE_liste = open("reddit_list.txt","r")
	liste = u.TxtToList(FILE_liste)
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
