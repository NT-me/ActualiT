# -*- coding: utf-8 -*-
from tinydb import TinyDB, Query
from FillmainCol.scrapers.utils import Article
import os

PATH_DB = str(os.getcwd()+"/mainCol.json")
db = TinyDB(PATH_DB)


def insertArticle(A):
    """
    Insert an article in the DB

    param -> Article
    return -> Document ID
    """
    if db.search(Query().titre == A.titre) == []:
        return db.insert(A.__dict__)
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
    DictArt = db.search(Query().ID == ID)
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
    listDict = db.all()

    res = list()

    for art in listDict:
        A = Article()
        for key in art:
            setattr(A, key, art[key])
        res.append(A)

    return res
