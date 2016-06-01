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

@route('/startup')
def index():
    return template('view/startup')

@route('/createProject')
def index():
    return template('view/create_project')

@route('/selectIndicator')
def index():
    #参数要带projectId,校验projectId是否存在

    #input = request.json
    print request
    return template('view/select_indicator')

@route('/listProject')
def index():
    print request

@route('/editSearchResult')
def index():
    print request
    #参数要带projectId
    #1.根据EMR_id, 查询EMR_full表，获取EMR_text, 展现在左侧
    #2.根据EMR_id, 查询EMR_indicator表，获取indicator, value，展现在右侧
    #3.保存按钮,提交修改的数据到EMR_indicator

@route('/exportIndicator')
def index():
    print request
    #参数要带projectId
    #1.根据projectId，查询project_EMR, EMR_indicator, project_indicator表，生产web报表，并且异步写成xls
    #2.导出按钮提供下载
 
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

@route('/select2/<filePath:path>')
def server_static(filePath):
    return static_file(filePath, root='./select2/')



@route('/etagger', method='POST')
def index():
    input = request.json
    a,b,c,d,e,f,h = es.etagger.tag(input['input'])
    print h
    return h

if __name__ == "__main__":
    es = ESSearch(SEARCH_HOST)
    es.initEtagger(entityDictName, entityDict, wordsegDict, mode)
    run(host='0.0.0.0', port=8080)
