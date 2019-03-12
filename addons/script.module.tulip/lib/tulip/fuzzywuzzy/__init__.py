# -*- coding: utf-8 -*-
__version__ = '0.17.0'

from tulip import control
from tulip.fuzzywuzzy import process

def wrapper(_list_, limit=5, score=70):

    results = []

    if not _list_:
        return

    term = control.inputDialog()

    if not term:
        return

    try:
        term = term.decode('utf-8')
    except AttributeError:
        pass

    control.busy()

    titles = [i['title'].encode('unicode-escape') for i in _list_]

    matches = [
        titles.index(l) for l, s in process.extract(
            term.encode('unicode-escape'), titles, limit=limit
        ) if s >= score
    ]

    for m in matches:
        results.append(_list_[m])

    control.idle()

    return results
