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

etagger = None

def getSearchResult(keywords):
    """
    @input keywords
    @return search List
    """
    global etagger

    (pos_tag, neg_tag) = etagger.tag(keywords)

    print "pos tag", u" ".join(list(pos_tag))
    print "neg tag", u" ".join(list(neg_tag))

    req = ' curl -s -XGET http://127.0.0.1:9200/1461044451/case/_search -d \'%s\''
    query_dict = {}
    query_dict["query"] = {}
    query_dict["query"]["bool"] = {}
    match_text = {}
    match_text["match_phrase"] = {}
    match_text["match_phrase"]["symp_text"] = {}
    match_text["match_phrase"]["symp_text"]["query"] = keywords
    match_text["match_phrase"]["symp_text"]["slop"] = 2
    if len(pos_tag | neg_tag) == 0:
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

    print query_dict
        
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
    cmd = req % (json.dumps(query_dict))
    ret, res = commands.getstatusoutput(cmd)
    
    res = json.loads(res)
    return res['hits']
 

@route('/')
def index():
    return template('view/index')

@route('/search')
def index():
    keywords = request.query.get('keywords')
    results = getSearchResult(keywords)
    return template('view/search', keywords = keywords, results= results)

@route('/show/<id>')
def index(id):
    return static_file(id +'.html', root='./html')


@route('/bootstrap/css/<filename>')
def server_static(filename):
    return static_file(filename, root='./bootstrap/css')

@route('/bootstrap/js/<filename>')
def server_static(filename):
    return static_file(filename, root='./bootstrap/js')


if __name__ == "__main__":
    global etagger
    edict = EntityDict("symp")
    edict.load_file("../mining/entity_tag/data/zhichangai_symp.csv")
    etagger = EntityTagger(edict, "/home/cihang/project/EMR_search_demo_trunk/mining/entity_tag/dict/wordseg_dict/", "query")

    run(host='localhost', port=8080)
