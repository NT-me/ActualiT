# -*- coding: utf-8 -*-
from tinydb import TinyDB, Query, where
import json
from objects.article import Article
from objects.source import Source
from FillmainCol.scrapers import utils as u
import time

#PATH_DB = str(os.getcwd()+"/mainCol.json")
#db = TinyDB(PATH_DB)
#artDB = db.table('articles')
#sourcesDB = db.table('sources')

artDB = TinyDB("mainCol.json")
sourcesDB = TinyDB("Sdb.json")


# Source methods
def insertSource(S):
    """
    Insert an source in the db

    param -> Article
    return -> Document ID
    """
    sourcesDB = TinyDB("Sdb.json")
    if sourcesDB.search(Query().ID == S.ID) == []:
        return sourcesDB.insert(S.__dict__)
    else:
        return -1


def insertSources(L):
    """
    Insert an source in the DB

    param -> List with sources
    return -> List with document ID
    """
    sourcesDB = TinyDB("Sdb.json")
    res = list()
    for item in L:
        if type(item) != Source:
            print(item)
            raise ValueError("Items in lists are not Source")
            sourcesDB.close()
            return -1
        res.append(insertArticle(item))

    sourcesDB.close()
    return res


def readSource(ID):
    """
    Take back an source from DB

    ID -> Source ID
    return -> The Source requested
    """
    sourcesDB = TinyDB("Sdb.json")
    S = Source()
    Qsource = Query()
    DictSou = sourcesDB.search(Qsource["ID"] == ID)
    if DictSou == []:
        sourcesDB.close()
        return -1
    else:
        for key in DictSou[0]:
            setattr(S, key, DictSou[0][key])

    sourcesDB.close()
    return S


def readSources(LID):
    """
    Take back an sources's list

    param -> ID list
    return -> Sources list
    """
    res = list()
    for id in LID:
        s = readSource(id)
        if type(s) == Source:
            res.append(s)
    return res


def readAllSources():
    """
    Return an list with all sources
    """
    sourcesDB = TinyDB("Sdb.json")
    listDict = sourcesDB.all()

    res = list()

    for sou in listDict:
        S = Source()
        for key in sou:
            setattr(S, key, sou[key])
        res.append(S)

    sourcesDB.close()
    return res


def readOriginSources(origin):
    sourcesDB = TinyDB("Sdb.json")
    try:
        listDict = sourcesDB.search(where('origin') == origin)
    except json.decoder.JSONDecodeError as e:
        print(str(e) + "\n")
        listDict = list()

    res = list()
    #print(origin + str(listDict))
    if listDict == []:
        #sourcesDB.close()
        return res

    for sou in listDict:
        S = Source()
        for key in sou:
            setattr(S, key, sou[key])
        res.append(S)
    sourcesDB.close()
    return res


def suprSource(ID):
    l = list()
    sourcesDB = TinyDB("Sdb.json")
    artDB = TinyDB("mainCol.json")

    # Delete source
    Sitem = sourcesDB.get(Query().ID == ID)
    l.append(Sitem.doc_id)
    sourcesDB.remove(doc_ids=l)
    sourcesDB.close()

    # Delete Articles
    #Sitem = sourcesDB.get(Query().ID == ID)
    #l.append(Sitem.doc_id)
    #sourcesDB.remove(doc_ids=l)
    #sourcesDB.close()

def modSource(ID, field, newValue):
    sourcesDB = TinyDB("Sdb.json")
    item_doc_id = sourcesDB.get(Query().ID == ID).doc_id
    l = list()
    l.append(item_doc_id)
    sourcesDB.update({field: newValue}, doc_ids = l)
    sourcesDB.close()


# Articles methods
def insertArticle(A, inIAs=False):
    """
    Insert an article in the DB

    param -> Article and if it's in insertArticles()
    return -> Document ID
    """
    if artDB.search(Query().titre == A.titre) == []:
        if not inIAs:
            artDB.close()
        return artDB.insert(A.__dict__)
    else:
        if not inIAs:
            artDB.close()
        return -1


@u.MTime
def insertArticles(L):
    """
    Insert an article in the DB

    param -> List with article
    return -> List with document ID
    """
    artDB = TinyDB("mainCol.json")
    res = list()
    for item in L:
        if type(item) != Article:
            raise ValueError("Items in lists are not Article")
            return -1
        res.append(insertArticle(item, True))
    artDB.close()

    return res


def readArticle(ID):
    """
    Take back an article from DB

    ID -> article object
    return -> The Article requested
    """
    artDB = TinyDB("mainCol.json")
    A = Article()
    DictArt = artDB.search(Query().ID == ID)
    if DictArt == []:
        artDB.close()
        return -1
    else:
        for key in DictArt[0]:
            setattr(A, key, DictArt[0][key])

    artDB.close()
    return A


def readArticles(LID):
    """
    Take back an article's list

    param -> ID list
    return -> Article list
    """
    res = list()
    for id in LID:
        a = readArticle(id)
        if type(a) == Article:
            res.append(a)

    return res


def readAllArticles():
    """
    Return an list with all articles
    """
    artDB = TinyDB("mainCol.json")

    listDict = artDB.all()

    res = list()

    for art in listDict:
        A = Article()
        for key in art:
            setattr(A, key, art[key])
        res.append(A)

    artDB.close()
    return res


@u.MTime
def deleteArticlesTooOld(artList, timeLimit):
    listA = list()
    listRES = list()
    artDB = TinyDB("mainCol.json")
    for art in artList:
        if art.date < time.time() - timeLimit and type(art) == Article:
            el = artDB.get(Query().ID == art.ID)
            listA.append(el.doc_id)
        else:
            listRES.append(art)
    try:
        artDB.remove(doc_ids=listA)
    except KeyError:
        pass

    return listRES
