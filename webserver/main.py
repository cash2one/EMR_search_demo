#encoding=utf8
from bottle import route, run, template, static_file, request, redirect
import json
import commands


def getSearchResult(keywords):
    """
    @input keywords
    @return search List
    """
    must = keywords
    must_not = '腹泻'
    should_1 = '便秘'
    should_2 = '呕血'
    #sample code
    req = ' curl -s -XGET http://127.0.0.1:9200/1461044451/case/_search -d \'%s\''
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



run(host='localhost', port=8080)
