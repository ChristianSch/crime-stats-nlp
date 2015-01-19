# TODO
* Tile paragraphs (http://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.texttiling)
* Tag paragraphs (location/crime) with NER (http://textminingonline.com/how-to-use-stanford-named-entity-recognizer-ner-in-python-nltk-and-other-programming-languages)
* sources: http://www.presseportal.de/polizeipresse/pm/43559/2758035/pol-gi-pressemeldung-vom-10-06-2014 and other stories

## Dependencies
To run the code you need the following packages:
* [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
* unicodecsv

## Acknowledgements
This work heavily relies on the [Stanford Named Entity Tagger](http://nlp.stanford.edu/software/CRF-NER.shtml) and the [german models](http://www.nlpado.de/~sebastian/software/ner_german.shtml) for it.

## Problems
If you get errors like this:
```
LookupError: 
**********************************************************************
  Resource u'corpora/stopwords' not found.  Please use the NLTK
  Downloader to obtain the resource:  >>> nltk.download()
  Searched in:
    - '/Users/username/nltk_data'
    - '/usr/share/nltk_data'
    - '/usr/local/share/nltk_data'
    - '/usr/lib/nltk_data'
    - '/usr/local/lib/nltk_data'
**********************************************************************
```

You should run
```
>>> import ntlk
>>> nltk.download()
```
in the Python interpreter and download the resource described above.