import json
from newsapi import NewsApiClient

#Chemin pour le json resultat:
PATH_FileRes = "newsapi.json"

#Clef d'api de NewsApiClient
API_Key_NAC = open("config/api_key", "r").read().replace("\n","")

def askNAC():
	# Init
	newsapi = NewsApiClient(api_key=API_Key_NAC)

	# /v2/top-headlines
	top_headlines = newsapi.get_top_headlines()
	for item in top_headlines["articles"]:
		item["from"]="newsAPI"

	with open(PATH_FileRes, 'w') as f:
		f.write(json.dumps(top_headlines, indent=4))
