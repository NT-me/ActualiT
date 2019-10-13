# -*- coding: utf-8 -*-
from tinydb import TinyDB, Query
from objects.article import Article
from objects.source import Source
import os

PATH_DB = str(os.getcwd()+"/mainCol.json")
db = TinyDB(PATH_DB)
artDB = db.table('articles')
sourcesDB = db.table('sources')

# Source methods
def insertSource(S):
    """
    Insert an source in the db

    param -> Article
    return -> Document ID
    """
    if sourcesDB.search(Query().ID == S.ID) == []:
        return sourcesDB.insert(S.__dict__)
    else :
        return -1


def insertSources(L):
    """
    Insert an source in the DB

    param -> List with sources
    return -> List with document ID
    """
    res = list()
    for item in L:
        if type(item) != Source:
            print(item)
            raise ValueError("Items in lists are not Source")
            return -1
        res.append(insertArticle(item))
    return res


def readSource(ID):
    """
    Take back an source from DB

    ID -> Source ID
    return -> The Source requested
    """
    S = Source()
    DictSou = sourcesDB.search(Query().ID == ID)
    if DictSou == []:
        return -1
    else:
        for key in DictSou[0]:
            setattr(A, key, DictSou[0][key])

    return S


def readArticles(LID):
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
    listDict = sourcesDB.all()

    res = list()

    for sou in listDict:
        S = Source()
        for key in sou:
            setattr(S, key, sou[key])
        res.append(S)

    return res

def readOriginSources(origin):
    listDict = sourcesDB.search(Query().origin == origin)
    res = list()

    for sou in listDict:
        S = Source()
        for key in sou:
            setattr(S, key, sou[key])
        res.append(S)
    return res

# Articles methods
def insertArticle(A):
    """
    Insert an article in the DB

    param -> Article
    return -> Document ID
    """
    if artDB.search(Query().titre == A.titre) == []:
        return artDB.insert(A.__dict__)
    else:
        return -1


def insertArticles(L):
    """
    Insert an article in the DB

    param -> List with article
    return -> List with document ID
    """
    res = list()
    for item in L:
        if type(item) != Article:
            print(item)
            raise ValueError("Items in lists are not Article")
            return -1
        res.append(insertArticle(item))
    return res


def readArticle(ID):
    """
    Take back an article from DB

    ID -> article object
    return -> The Article requested
    """
    A = Article()
    DictArt = artDB.search(Query().ID == ID)
    if DictArt == []:
        return -1
    else:
        for key in DictArt[0]:
            setattr(A, key, DictArt[0][key])

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
    listDict = artDB.all()

    res = list()

    for art in listDict:
        A = Article()
        for key in art:
            setattr(A, key, art[key])
        res.append(A)

    return res
