from yattag import Doc


def model(Title='', Summary='', Source='', Author='', Link=''):
    doc, tag, text, line = Doc().ttl()

    with tag('html'):
        with tag('body'):
            line('h1', Title)
            if Author != '' :
                line('h2', Author)
            else:
                line('h2', Source)

            with tag('div', klass = 'description'):
                text(Summary)
                line('a', Link)
    return doc.getvalue()
