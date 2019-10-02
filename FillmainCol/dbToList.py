# -*- coding: utf-8 -*-
from FillmainCol import wrapperDB as wdb
from FillmainCol.scrapers.utils import Article
from tinydb import TinyDB
import time


def sortMainCol():
    db = TinyDB(wdb.PATH_DB)

    len_DB = len(db)

    ListA = []
    ListeR = []
    i = 0

    def getDate(article):
        return article.date

    # ListeA contient les articles sous forme d'objet
    while i < len_DB:
        artDB = db.all()[i]
        if artDB["date"] > time.time() - 604800:
            ListA.append(Article(artDB["ID"], artDB["titre"], artDB["auteur"], artDB["info_source"], artDB["lien"], artDB["resume"], artDB["lien_img"], artDB["date"], artDB["module_source"]))
        else:
            ListeR.append(i)
        i += 1
    try:
        db.remove(doc_ids=ListeR)
    except:
            pass
    return sorted(ListA, key=getDate, reverse=True)
