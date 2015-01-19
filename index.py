#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division

from bs4 import BeautifulSoup
from nltk.tag.stanford import NERTagger
from nltk.tokenize.texttiling import TextTilingTokenizer

from lib import *

BASE_LINK = 'http://www.presseportal.de/polizeipresse/pm/43559/polizeipraesidium-mittelhessen-giessen'

st = NERTagger('stanford-ner-2012-05-22-german/dewac_175m_600.crf.ser.gz',
    'stanford-ner.jar')
tokenizer = TextTilingTokenizer()

data = []

try:
    articles = read_articles_from_csv()
except Exception, e:
    articles = get_all_articles_for_base_url(BASE_LINK)
    dump_articles_to_csv(articles) # cache
else:
    if (len(articles) == 0):
        articles = get_all_articles_for_base_url(BASE_LINK)
        dump_articles_to_csv(articles) # cache

# for article in articles:
    # print(len(article))
    # TODO: this does not work as good as expected!
    # tiles = tokenizer.tokenize(article)

    # testing
    # tag = st.tag(tiles[0].encode('utf-8').split())

    # TODO: NER wants to output ascii and crashes?
    # data.append(tag)

    # for tile in tiles:
        # let the stanford NER tag entities
        # data.append(st.tag(tile.encode('utf-8')))
        # print('\n## ' + tile) # DEBUG

# print(data[0]) # DEBUG

# TODO: find crime per tile; if none => ignore