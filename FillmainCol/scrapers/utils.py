from dateutil import parser as c
from datetime import datetime as dt
from time import process_time


PATH_DB = "mainCol.json"


class Article:
    def __init__(self, ID=None, titre=None, auteur=None, info_source=None, lien=None, resume=None, lien_img=None, date=None, module_source=None):
        self.titre = titre
        self.ID = ID
        self.auteur = auteur
        self.info_source = info_source
        self.lien = lien
        self.resume = resume
        self.lien_img = lien_img
        self.date = date
        self.module_source = module_source


def MTime(func):
    def wrapper(*args, **kwargs):
        t = process_time()
        response = func(*args, **kwargs)
        elapsed_time = process_time() - t
        Fname = str(func.__name__)
        elapsed_time = str(elapsed_time)
        print("-= " + Fname + " : " + elapsed_time + "\n")
        return response
    return wrapper


def TxtToList(f):
    """
    Permet de transformer un fichier txt en une liste python
    """
    res = []

    ligne = f.readline()
    while ligne != "":
        ligne = ligne.replace("\n", "")
        res.append(ligne)
        ligne = f.readline()
    f.close()

    return res


def convert_time(time):
    return dt.timestamp(c.parse(str(time)))
