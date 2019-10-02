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
            raise ValueError("Items in lists are not Article")
            return -1
        res.append(insertArticle(item))
    return res

def readArticle(ID):
    """
    ID -> article object
    """
    pass
