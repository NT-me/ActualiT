# -*- coding: utf-8 -*-

import utils as u
from tinydb import TinyDB


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
    i = 0

    def getDate(article):
        return article.date

    # ListeA contient les articles sous forme d'objet
    while i < len_DB:
        artDB = db.all()[i]
        ListA.append(Article(artDB["ID"], artDB["Titre"], artDB["Auteur"], artDB["info_source"], artDB["Lien"], artDB["Contenu"], artDB["URL_image"], artDB["Publication"], artDB["module_source"]))
        i += 1

    return sorted(ListA, key=getDate)
