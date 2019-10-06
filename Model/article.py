from yattag import Doc
from FillmainCol.scrapers import utils as u
from PyQt5 import QtGui, QtCore
import urllib.request


def model(A):
    doc, tag, text, line = Doc().ttl()
    try:
        with tag('html'):
            with tag('body'):
                # Download the image
                if A.lien_img is not None and A.lien_img != '':
                    try:
                        urllib.request.urlretrieve(A.lien_img, "cache/articleImg.png")
                        with tag('div', klass='Front image'):
                            doc.stag('img', align="middle", height='300', src='cache/articleImg.png')
                    except:
                        pass
                line('h1', A.titre)
                if A.auteur is not None:
                    line('b', A.auteur)
                else:
                    line('b', A.info_source)

                with tag('div', klass = 'description'):
                    text(A.resume)

                with tag('a', href=A.lien):
                    line('b', '\nEn voir plus...')
    except TypeError as e:
        print(e)
    return doc.getvalue()
