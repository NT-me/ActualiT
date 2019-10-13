from objects.source import Source
from FillmainCol import wrapperDB as wdb

def URLPurifier(str):
    # 1st point
    str = str[str.find('.')+1:]
    # 2nd point
    str = str[:str.find('.')]

    return str

def add(url, origin):
    ID = hash(url)
    if origin == "RSS" or origin == "Reddit":
        name = URLPurifier(url)
    elif origin == "Twitter":
        if url[0] != "@":
            name = "@" + url
    S = Source(ID, name, url, origin)
    wdb.insertSource(S)
    print("source OK\n")
