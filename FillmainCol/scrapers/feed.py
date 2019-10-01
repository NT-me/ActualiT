import feedparser as fp
import json
from time import mktime
from . import utils as u


PATH_FileRes = "feedRES.json"


# Liste des feeds
def askFeeds():

	FILE_liste = open("FillmainCol/scrapers/feed_list.txt", "r")
	liste = u.TxtToList(FILE_liste)
	res = dict()
	inc = 0

	# Parcours la liste de source
	for item in liste:
		parse = fp.parse(item).entries
		res[inc] = parse
		# Ajoute la provenance à chaque article
		for article in res[inc]:
			article["from"] = "Feed RSS"
			article["source"] = item
			article["published"] = mktime(article["published_parsed"])
		inc = inc + 1

	with open(PATH_FileRes, 'w') as f:
		f.write(json.dumps(res, indent=4))
