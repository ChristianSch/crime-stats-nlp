#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import unicodecsv
from urlparse import urlparse, urljoin

from bs4 import BeautifulSoup

def normalize_url(base_url, url):
    """
    Returns ``url`` with protocol and domain taken from ``base_url``.

    Parameters
    ----------
    base_url: string
        Valid url that holds at least the protocol and hostname.

    url: string
        Path that creates a valid url when appended to a protocol and hostname.

    Returns
    -------
    Valid URL that consists of at least a protocol, a hostname and path.

    Examples
    --------
    >>> normalize_url('http://www.presseportal.de/polizeipresse/pm/43559/polizeipraesidium-mittelhessen-giessen',
        '/polizeipresse/pm/43559/2929634/pol-gi-pressemitteilung-vom-19-01-2015-autoaufbrueche-in-giessen-und-luetzellinden-handys-geklaut')
    'http://www.presseportal.de/polizeipresse/pm/43559/2929634/pol-gi-pressemitteilung-vom-19-01-2015-autoaufbrueche-in-giessen-und-luetzellinden-handys-geklaut'

    """
    parsed_url = urlparse(url)
    parsed_base = urlparse(base_url)

    url = urljoin(parsed_base.scheme + '://' + parsed_base.netloc, url)

    return url

def get_pagination_links_for_base_url(base_url):
    """
    Get pagination links that each link to a paginated article overview page
    on ``http://www.presseportal.de``.

    Parameters
    ----------
    base_url: string
        Valid url from ``http://www.presseportal.de``.

    Returns
    -------
    Set of unicode encoded urls that each link to a paginated article overview 
    page.

    Examples
    --------
    >>> get_pagination_links_for_base_url('http://www.presseportal.de/polizeipresse/pm/43559/polizeipraesidium-mittelhessen-giessen')
    set([u'http://www.presseportal.de/polizeipresse/pm/43559/polizeipraesidium-mittelhessen-giessen?start=162',
        …
        u'http://www.presseportal.de/polizeipresse/pm/43559/polizeipraesidium-mittelhessen-giessen?start=27',
        u'http://www.presseportal.de/polizeipresse/pm/43559/polizeipraesidium-mittelhessen-giessen?start=108'])
    """
    page_urls = set()

    base_soup = BeautifulSoup(urllib2.urlopen(base_url).read())
    paginated_soup = base_soup.find('div', attrs={'class':'pagination'})

    # Parse out all the paginated urls
    for ahref in paginated_soup.find_all('a', attrs={'class':'pagination-link'}):
        # it seems that they use urls without the domain. let's add those
        page_urls.add(normalize_url(base_url, ahref.get('href')))

    return page_urls

def get_article_links_from_paginated_pages(page_urls):
    """
    Get article links from pagination page on ``http://www.presseportal.de``.

    Parameters
    ----------
    page_urls: array_like
        Array of valid url from ``http://www.presseportal.de`` linking to a
        paginated article overview.

    Returns
    -------
    Set of unicode encoded urls that each link to an article.

    Examples
    --------
    >>> get_article_links_from_paginated_pages(['http://www.presseportal.de/polizeipresse/pm/43559/polizeipraesidium-mittelhessen-giessen?start=162'])
    set([u'http://www.presseportal.de/polizeipresse/pm/43559/2796378/pol-gi-pressemeldungen-vom-30-07-2014', 
        …
        u'http://www.presseportal.de/polizeipresse/pm/43559/2816128/pol-gi-pressemeldung-vom-26-08-2014'])
    """
    article_urls = set()

    for page_url in page_urls:
        page_soup = BeautifulSoup(urllib2.urlopen(page_url).read())

        for article in page_soup.find_all('article', attrs={'class':'news'}):
            article_urls.add(normalize_url(page_url, article.get('data-url')))

    return article_urls

def get_article_text_for_article_url(article_url):
    """
    Extracts the article text on an article on ``http://www.presseportal.de``.

    Parameters
    ----------
    page_urls: string
        Valid article URL on ``http://www.presseportal.de``.

    Returns
    -------
    Unicode string containing the article text
    """
    article_text = ""
    article_soup = BeautifulSoup(urllib2.urlopen(article_url).read())
    pars = article_soup.find('div', attrs={'class':'story-text'}).find_all('p')

    for par in pars:
        article_text += par.text + '\n'
    
    return article_text

def get_all_articles_for_base_url(base_url):
    """
    Extracts all article texts on a police station subpage of
    ``http://www.presseportal.de`` like
    ``http://www.presseportal.de/polizeipresse/pm/43559/polizeipraesidium-mittelhessen-giessen``.

    Parameters
    ----------
    base_url: string
        Valid URL of the police station subpage on ``http://www.presseportal.de``.

    Returns
    -------
    Collection of article texts
    """
    articles = []
    page_urls = get_pagination_links_for_base_url(base_url)
    article_urls = get_article_links_from_paginated_pages(page_urls)

    for article_url in article_urls:
        artcl = get_article_text_for_article_url(article_url)

        if (len(artcl) > 10):
            articles.append(artcl)

    return articles

def dump_articles_to_csv(articles, file_name='test-data/article-text.csv'):
    """
    Dumps extracted articles to a csv file to cache and save them.

    Parameters
    ----------
    articles: array_like
        collection of article texts as returned by
        ``get_all_articles_for_base_url``.

    file_name: string, optional
        path (with filename) to the csv file the articles shall be saved to
        (default is ``test-data/article-text.csv``)

    See Also
    --------
    read_articles_from_csv: read articles from csv
    get_all_articles_for_base_url: fetch article texts from the internet
    """
    with open(file_name, 'wb') as csvfile:
        the_writer = unicodecsv.writer(csvfile, quoting=unicodecsv.QUOTE_ALL)

        for article in articles:
            the_writer.writerow(article)

def read_articles_from_csv(file_name='test-data/article-text.csv'):
    """
    Reads article texts from csv file.

    Parameters
    ----------
    file_name: string, optional
        path (with filename) to the csv file the articles shall be saved to
        (default is ``test-data/article-text.csv``)

    Returns
    -------
    Collection of article texts

    See Also
    --------
    dump_articles_to_csv: dump articles to csv
    get_all_articles_for_base_url: fetch article texts from the internet
    """
    artcls = []

    with open(file_name, 'rb') as csvfile:
        the_reader = unicodecsv.reader(csvfile, quoting=unicodecsv.QUOTE_ALL)

        for row in the_reader:
            artcls.append(row)

    return artcls