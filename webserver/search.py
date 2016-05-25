#encoding=utf8
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../lib")
from bottle import route, run, template, static_file, request, redirect
from config import Config

config = Config("./conf/search.conf")
entitySrc= config.get("etagger", "entity_src")
sys.path.append(entitySrc)

from essearch import ESSearch

BATCH = config.get("search", "batch")
SEARCH_HOST = config.get("search", "host")
SEARCH_TYPE = config.get("search", "type")

entityDictName = config.get("etagger", "entity_dict_name")
entityDict = config.get("etagger", "entity_dict")
wordsegDict = config.get("etagger", "wordseg_dict")
mode = config.get("etagger", "mode")

global es

@route('/')
def index():
    return template('view/index')

@route('/search')
def index():
    keywords = request.query.get('keywords')
    pn = 0
    pageSize = 10
    if 'pn' in request.query:
        pn = int(request.query.get('pn'))
        pn = (pn/10)*10

    #call search in essearch in lib/essearch.py
    results = es.search(keywords, BATCH, SEARCH_TYPE, pn, pageSize)
    return template('view/search', keywords = keywords, pn = pn, results= results)

@route('/show/<id>')
def index(id):
    return static_file(id +'.html', root='./html')

@route('/bootstrap/css/<filename>')
def server_static(filename):
    return static_file(filename, root='./bootstrap/css')

@route('/bootstrap/js/<filename>')
def server_static(filename):
    return static_file(filename, root='./bootstrap/js')

@route('/etagger', method='POST')
def index():
    input = request.json
    es.etagger.tag(input['input'], input['output'])


if __name__ == "__main__":
    es = ESSearch(SEARCH_HOST)
    es.initEtagger(entityDictName, entityDict, wordsegDict, mode)
    run(host='0.0.0.0', port=8080)
