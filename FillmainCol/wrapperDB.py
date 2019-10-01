# -*- coding: utf-8 -*-
from tinydb import TinyDB
import os

PATH_DB = str(os.getcwd()+"/mainCol.json")
db = TinyDB(PATH_DB)


def insertArticle():
    pass


def readArticle():
    """
    id -> article object
    """
    pass
