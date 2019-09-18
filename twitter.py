import twitter_scraper as ts
import json
import utils as u

PATH_FileRes = "tweetRES.json"
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


def askTwitter():
	#Liste des tweet
	FILE_liste = open("twitter_list.txt","r")

	liste = TxtToList(FILE_liste)
	res = dict()
	inc = 0

	#Parcours la liste de source
	for item in liste:
		parse = ts.get_tweets(item, pages=1)
		for tweet in parse:
			res[inc]=tweet
			res[inc]["time"]=u.convert_time(res[inc]["time"])
			res[inc]["from"]="twitter"
			res[inc]["author"]=item



			inc = inc + 1

	with open(PATH_FileRes, 'w') as f:
		f.write(json.dumps(res, indent=4))
