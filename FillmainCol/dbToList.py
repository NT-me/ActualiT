# -*- coding: utf-8 -*-

from FillmainCol.scrapers import utils as u
from tinydb import TinyDB
import time


class Article:
    def __init__(self, ID, titre, auteur, info_source, lien, resume, lien_img, date, module_source):
        self.ID = ID
        self.titre = titre
        self.auteur = auteur
        self.info_source = info_source
        self.lien = lien
        self.resume = resume
        self.lien_img = lien_img
        self.date = date
        self.module_source = module_source


def sortMainCol():
    db = TinyDB(u.PATH_DB)

    len_DB = len(db)

    ListA = []
    ListeR = []
    i = 0

    def getDate(article):
        return article.date

    # ListeA contient les articles sous forme d'objet
    while i < len_DB:
        artDB = db.all()[i]
        if artDB["Publication"] > time.time() - 604800:
            ListA.append(Article(artDB["ID"], artDB["Titre"], artDB["Auteur"], artDB["info_source"], artDB["Lien"], artDB["Contenu"], artDB["URL_image"], artDB["Publication"], artDB["module_source"]))
        else:
            ListeR.append(i)
        i += 1
    try:
        db.remove(doc_ids=ListeR)
    except :
            pass
    return sorted(ListA, key=getDate, reverse=True)
