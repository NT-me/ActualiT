import feedparser as fp
import json
from time import mktime
from . import utils as u
from FillmainCol import wrapperDB as wdb


PATH_FileRes = "feedRES.json"


# Liste des feeds
def askFeeds():

	liste = wdb.readOriginSources('RSS')
	res = dict()
	inc = 0

	# Parcours la liste de source
	if liste != []:
		for item in liste:
			parse = fp.parse(item.link).entries
			res[inc] = parse
			# Ajoute la provenance à chaque article
			for article in res[inc]:
				article["from"] = "Feed RSS"
				article["source"] = item.name
				article["published"] = mktime(article["published_parsed"])
			inc = inc + 1

	with open(PATH_FileRes, 'w') as f:
		f.write(json.dumps(res, indent=4))
