#encoding=utf8
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../mining/entity_tag/src/")
from bottle import route, run, template, static_file, request, redirect
import json
import commands
from entity_dict import *
from entity_tag import *
from config import Config
config = Config("./conf/search.conf")
BATCH = config.get("search", "batch")
SEARCH_HOST = config.get("search", "host")
SEARCH_TYPE = config.get("search", "type")

global etagger
etagger = None


def queryBuilder(keywords):
    """
    @input keywords
    @output query in json 
    """
    #sample
    '''
    query = {
        "query":{
            "bool":{
                "must": { "match": {"symp_tag":must}},
                "must_not": {"match": {"symp_text": must_not}},
                "should": [
                    {"match":{"symp_text":should_1}},
                    {"match":{"symp_text":should_2}}
                ]
            }
        }
    }
    '''

    global etagger

    (pos_tag, neg_tag, polarity_res, range_lower, range_upper, kv_res, kvs_res, mk_str) = etagger.tag(keywords)

    print "keywords", keywords
    print "pos tag", u" ".join(list(pos_tag))
    print "neg tag", u" ".join(list(neg_tag))
    for key in polarity_res:
        print "search.py", key + "\t" + polarity_res[key]

    query_dict = {}
    query_dict["query"] = {}
    query_dict["query"]["bool"] = {}
    match_text = {}
    match_text["match_phrase"] = {}
    match_text["match_phrase"]["symp_text"] = {}
    match_text["match_phrase"]["symp_text"]["query"] = keywords
    match_text["match_phrase"]["symp_text"]["slop"] = 2
    polarity_flag = True
    for key in polarity_res:
        if polarity_res != "":
            polarity_falg = False
    if len(pos_tag | neg_tag) == 0 and polarity_flag:
        query_dict["query"]["bool"]["must"] = match_text
    else:
        query_dict["query"]["bool"]["should"] = []
        #query_dict["query"]["bool"]["should"].append(match_text)
        query_dict["query"]["bool"]["should"].append({})
        tag_bool_query = query_dict["query"]["bool"]["should"][-1]
        tag_bool_query["bool"] = {}
        tag_bool_query["bool"]["must"] = []
        for tag in pos_tag:
            tag_bool_query["bool"]["must"].append({})
            s = tag_bool_query["bool"]["must"][-1]
            s["match"] = {}
            s["match"]["symp_pos_tag"] = tag.encode("utf8")
        for tag in neg_tag:
            tag_bool_query["bool"]["must"].append({})
            s = tag_bool_query["bool"]["must"][-1]
            s["match"] = {}
            s["match"]["symp_neg_tag"] = tag.encode("utf8")
        for key in polarity_res:
            if polarity_res[key] == "":
                continue
            print "search.py polarity_res[key]", len(polarity_res[key])
            tag_bool_query["bool"]["must"].append({})
            s = tag_bool_query["bool"]["must"][-1]
            s["match"] = {}
            s["match"][key] = polarity_res[key].encode("utf8")


    print json.dumps(query_dict)
    return query_dict
 

def getSearchResult(keywords, pn):
    """
    @input keywords
    @return search List
    """
       
    baseUrl = "http://%(host)s/%(batch)s/%(type)s/_search" %{"host":SEARCH_HOST, "batch":BATCH, "type":SEARCH_TYPE}

    req = ' curl -s -XGET '+ baseUrl + ' -d \'%s\''

    query = queryBuilder(keywords)
    pn = (pn/10)*10
    query["from"] = 0 if pn == 0 else (pn-10)
    query["size"] = 10
    cmd = req % (json.dumps(query))
    ret, res = commands.getstatusoutput(cmd)
    
    res = json.loads(res)
    return res['hits']
 

@route('/')
def index():
    return template('view/index')

@route('/search')
def index():
    keywords = request.query.get('keywords')
    pn = 10
    pageSize = 10
    if 'pn' in request.query:
        pn = int(request.query.get('pn'))
    results = getSearchResult(keywords, pn)
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
    etagger.tag(input['input'], input['output'])


if __name__ == "__main__":
    edict = EntityDict("symp")
    #edict.load_file("../mining/entity_tag/data/zhichangai_symp.csv")
    edict.load_file("../mining/entity_tag/data/class_term.dict.gbk")
    patternList = Pattern().getPattern()
    etagger = EntityTagger(edict, patternList, "/home/yongsheng/EMR_search_demo/mining/entity_tag/dict/wordseg_dict/", "query")

    run(host='0.0.0.0', port=8080)
