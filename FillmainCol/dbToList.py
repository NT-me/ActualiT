# -*- coding: utf-8 -*-
from FillmainCol import wrapperDB as wdb
from FillmainCol.scrapers.utils import Article
from tinydb import TinyDB
import time


def sortMainCol():
    db = TinyDB(wdb.PATH_DB)

    ListA = []
    ListeR = []
    i = 0

    def getDate(article):
        return article.date

    # ListeA contient les articles sous forme d'objet
    a = iter(db)
    for i in a:
        try:
            artDB = wdb.readArticle(next(a)["ID"])
        except StopIteration:
            pass
        if artDB.date > time.time() - 604800 and type(artDB) == Article:
            ListA.append(artDB)
        else:
            ListeR.append(i)

    try:
        db.remove(doc_ids=ListeR)
    except:
            pass
    return sorted(ListA, key=getDate, reverse=True)
