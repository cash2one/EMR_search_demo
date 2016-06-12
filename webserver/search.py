#encoding=utf8
# -*- coding: utf-8 -*-
import sys
reload(sys)
import traceback
sys.setdefaultencoding('utf-8')
sys.path.append("../lib")
import csv
from bottle import route, run, template, static_file, request, redirect
from config import Config
from Mysql import Mysql,MySQLdb


from essearch import ESSearch

config = Config("./conf/search.conf")
BATCH = config.get("search", "batch")
SEARCH_HOST = config.get("search", "host")
SEARCH_TYPE = config.get("search", "type")

etaggerHost = config.get("etagger", "host")
etaggerTimeout = int(config.get("etagger", "timeout"))
mode = config.get("etagger", "mode")

MYSQL_HOST = config.get("mysql", "host")
USER = config.get("mysql", "user")
PASSWD = config.get("mysql", "passwd")
DB = "hospital"

global es

@route('/')
def index():
    return template('view/startup')

@route('/startup')
def index():
    return template('view/startup')

@route('/createProject')
def index():
    return template('view/create_project')

@route('/selectIndicator')
def index():
    query = request.query
    # name
    proj_name = query.get('projectname')
    if not proj_name:
        print "error: proj_name has not been set"
    proj_name = proj_name.strip()
    if proj_name == "":
        print "error: proj_name can not be empty string"
    
    # detail
    proj_detail = query.get('detail').strip()
    if not proj_detail:
        print "error: proj_detail has not been set"
    proj_detail = proj_detail.strip()
    if proj_detail == "":
        print "error: proj_detail can not be empty string"

    # owner
    proj_owner = query.get('owner').strip()
    if not proj_owner:
        print "error: proj_owner has not been set"
    proj_owner = proj_owner.strip()
    if proj_owner == "":
        print "error: proj_owner can not be empty string"

    proj_id = -1
    # save
    try:
        mysql = Mysql(db = DB,
                    host = MYSQL_HOST,
                    user = USER,
                    passwd = PASSWD)
        mysql.connect()

        # check if duplicated
        sql = "select project_id from project where name = \'%s\' and detail = \'%s\' and owner = \'%s\'" %(proj_name, proj_detail, proj_owner)
        print sql
        res = mysql.executeNoConn(sql)
        if len(res) > 0:
            print "error: project exists, please modify!"

        # insert and return project_id
        sql = "insert into project(name, detail, owner) values('%s', '%s', '%s')" %(proj_name, proj_detail, proj_owner)
        mysql.executeNoConn(sql)

        sql = "select project_id from project where name = '%s' and detail = '%s' and owner = '%s'" %(proj_name, proj_detail, proj_owner)
        res = mysql.executeNoConn(sql)

        proj_id = res[0][0]
        mysql.close()
    except MySQLdb.Error, e:
        print traceback.format_exc()
        mysql.close()
   
    return template('view/select_indicator', projectid = proj_id)

@route('/ajaxSelectIndicator', method="POST")
def index():
    projectid = request.json['projectid']
    indicators = request.json['indicator']

    try:
        mysql = Mysql(db = DB,
                    host = MYSQL_HOST,
                    user = USER,
                    passwd = PASSWD)
        mysql.connect()

        for idk in indicators:
            # check if exists
            idk = idk.strip().decode('utf8')
            sql = "select indicator_id from indicator where name = '%s'" %(idk,)
            print sql
            res = mysql.executeNoConn(sql)
            if len(res) > 0:
                idk_id = res[0][0]
            else:
                # insert and get indicator_id
                sql = "insert into indicator(name, type) values('%s', %s)" %(idk, 1)
                print sql
                mysql.executeNoConn(sql)
                sql = "select indicator_id from indicator where name = '%s'" %(idk,)
                print sql
                res = mysql.executeNoConn(sql)
                idk_id = res[0][0]

            # sav projectid & indicatorid
            sql = "insert into project_indicator values('%s', '%s')" %(projectid, idk_id)
            mysql.executeNoConn(sql)

        mysql.close()
    except MySQLdb.Error, e:
        print traceback.format_exc()
        mysql.close()
    return {'msg':'ok'}

@route('/listProject')
def index():
    print request

@route('/getIndicatorList', method="POST")
def index():
    indicators = []
    mysql = Mysql(db = DB,
                host = MYSQL_HOST,
                user = USER,
                passwd = PASSWD)

    sql = 'select name from indicator'
    rows = mysql.execute(sql)
    for row in rows:
        indicators.append(row[0])
    return {'msg':'ok', 'value':indicators}

@route('/editSearchResult')
def index():
    print request
    projectid = request.query.get('projectid')
    emrid = request.query.get('emrid')
    #参数要带projectId
    #1.根据EMR_id, 查询EMR_full表，获取EMR_text, 展现在左侧
    #2.根据EMR_id, 查询EMR_indicator表，获取indicator, value，展现在右侧
    #3.保存按钮,提交修改的数据到EMR_indicator

    indicator = {}
    try:
        mysql = Mysql(db = DB,
            host = MYSQL_HOST,
            user = USER,
            passwd = PASSWD)

        mysql.connect()

        try:
            sql = "select emr_id from emr where detail = '%s'" %(emrid,)
            res = mysql.executeNoConn(sql)
            print sql, res
            emr_id = res[0][0]
        except:
            pass

        sql = 'select indicator_id from project_indicator where project_id = %s' %(projectid,)
        idk_ids = []
        rows = mysql.executeNoConn(sql)
        for row in rows:
            idk_ids.append(row[0])

        for idk_id in idk_ids:
            sql = "select name from indicator where indicator_id = %s"  %(idk_id,)
            rows = mysql.executeNoConn(sql)
            name = rows[0][0]

            sql = "select value from emr_indicator where emr_id = %s and indicator_id = %s" %(emr_id, idk_id)
            rows = mysql.executeNoConn(sql)
            value = ""
            if len(rows) > 0:
                value = rows[0][0]
            indicator[name] = value

        mysql.close()
    except MySQLdb.Error, e:
        print traceback.format_exc()
        mysql.close()

    #indicator = {"血常规":5, "尿常规":7, "生化":12}
    return template('view/edit_search_result', projectid = projectid, emrid= emrid, indicator = indicator)

@route('/ajaxEditSearchResult', method="POST")
def index():
    #保存修改数据,写入数据库
    projectid = request.json['projectid']
    emrid = request.json['emrid']
    indicators = request.json['indicator']
    try:
        mysql = Mysql(db = DB,
                    host = MYSQL_HOST,
                    user = USER,
                    passwd = PASSWD)
        mysql.connect()

        sql = "select emr_id from emr where detail = '%s'" %(emrid,)
        res = mysql.executeNoConn(sql)
        emr_id = res[0][0]

        sql = "insert into project_emr values(%s, %s)" %(projectid, emr_id)
        print sql
        try:
            mysql.executeNoConn(sql)
        except:
            pass

        for idk in indicators:
            value = indicators[idk].strip()
            sql = "select indicator_id from indicator where name = '%s'" %(idk,)
            res = mysql.executeNoConn(sql)
            idk_id = res[0][0]

            # sav emr_id & ink_id
            sql = "insert into emr_indicator values(%s, %s, '%s')" %(emr_id, idk_id, value)
            print sql
            try:
                mysql.executeNoConn(sql)
            except:
                pass

        mysql.close()
    except MySQLdb.Error, e:
        print traceback.format_exc()
        mysql.close()

    return {'msg':'ok'}


@route('/exportIndicator')
def index():
    projectid = request.query.get('projectid')
    #参数要带projectId
    #1.根据projectId，查询project_EMR, EMR_indicator, project_indicator表，生产web报表，并且异步写成xls
    #2.导出按钮提供下载

    #emrid, indicator1, indicator2, ...

    try:
        mysql = Mysql(db = DB,
            host = MYSQL_HOST,
            user = USER,
            passwd = PASSWD)

        mysql.connect()
        sql = 'select emr_id from project_emr where project_id = %s' %(projectid,)
        emrids = []
        rows = mysql.executeNoConn(sql)
        for row in rows:
            emrids.append(row[0])

        sql = 'select indicator_id from project_indicator where project_id = %s' %(projectid,)
        idk_ids = []
        rows = mysql.executeNoConn(sql)
        for row in rows:
            idk_ids.append(row[0])

        fields = ['emrid']
        for idk_id in idk_ids:
            sql = "select name from indicator where indicator_id = %s"  %(idk_id,)
            rows = mysql.executeNoConn(sql)
            name = rows[0][0]
            fields.append(name)

        values = []
        for emrid in emrids:
            value = [emrid]
            for idk_id in idk_ids:
                sql = "select value from emr_indicator where emr_id = %s and indicator_id = %s" %(emrid, idk_id)
                rows = mysql.executeNoConn(sql)
                value.append(rows[0][0])
            values.append(value)
        mysql.close()
    except MySQLdb.Error, e:
        print traceback.format_exc()
        mysql.close()
    
    '''fields = ['emrid', '血常规', '尿常规', '生化']
    values = []
    values.append([4, 1.8, 2.7, 8.7])
    values.append([5, 1.8, 2.7, 8.7])
    values.append([6, 1.8, 2.7, 8.7])
    '''

    download = 'tmp/%s.csv' %(projectid)
    writer = csv.writer(file(download, 'wb'))
    writer.writerow(fields);
    for line in values:
        writer.writerow(line)
    return template('view/export_indicator', fields = fields, values = values, download=download)

 
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


@route('/newSearch')
def index():
    print request.url
    keywords = request.query.get('keywords')
    projectid = request.query.get('projectid')
    indicatorRange = {}
    for k in request.query:
        if k != 'keywords' and k != 'projectid' and k != 'pn':
            indicatorRange[k] = request.query.get(k).split(":")
    pn = 0
    pageSize = 10
    if 'pn' in request.query:
        pn = int(request.query.get('pn'))
        pn = (pn/10)*10

    #call search in essearch in lib/essearch.py
    print indicatorRange
    if keywords is None or len(keywords) == 0:
        results = {}
    else :
        results = es.search(keywords, indicatorRange, BATCH, SEARCH_TYPE, pn, pageSize)
    return template('view/new_search', keywords = keywords, indicatorRange = indicatorRange, projectid = projectid, pn = pn, results= results, url= request.url.split('&pn')[0])



@route('/show/<id>')
def index(id):
    return static_file(id +'.html', root='./html')

@route('/tmp/<filePath:path>')
def index(filePath):
    return static_file(filePath, root='./tmp')


@route('/bootstrap/<filePath:path>')
def server_static(filePath):
    return static_file(filePath, root='./bootstrap/')


@route('/select2/<filePath:path>')
def server_static(filePath):
    return static_file(filePath, root='./select2/')

@route('/bootstrap-table/<filePath:path>')
def server_static(filePath):
    return static_file(filePath, root='./bootstrap-table/')

if __name__ == "__main__":
    import zerorpc
    client = zerorpc.Client(timeout=etaggerTimeout)
    client.connect("tcp://%s" %(etaggerHost))
    es = ESSearch(SEARCH_HOST, client.tag)
    run(host='0.0.0.0', port=8080)
    client.close()
