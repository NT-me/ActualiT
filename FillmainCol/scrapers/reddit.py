import feedparser as fp
import json
from . import utils as u
from FillmainCol import wrapperDB as wdb

PATH_FileRes = "redditRES.json"


def askReddit():
	# Liste des feeds
	liste = wdb.readOriginSources('Reddit')
	res = dict()
	inc = 0

	# Parcours la liste de source
	for item in liste:
		if item.link[len(item.link)-1] == '/':
			item = item.link[:len(item.link)-1]+".rss"
		else:
			item = item+".rss"
		parse = fp.parse(item).entries
		res[inc] = parse
		# Ajoute la provenance à chaque article
		for article in res[inc]:
			article["from"] = "reddit"
		inc = inc + 1

	with open(PATH_FileRes, 'w') as f:
		f.write(json.dumps(res, indent=4))
