#encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../lib/")
sys.path.append("../rpc-service/gen-py")
sys.path.append("../rpc-service/")
import json
import os
from multiprocessing import Pool

from tag import Tagger
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import time

from config import Config
import traceback
from collections import OrderedDict
#from esindex import ESIndex
from mongo import Mongo
import random

global mongo_host, mongo_port, mongo_table, mongo_db

class TaggerClient():
    def __init__(self, ip, port):
        self.transport = TSocket.TSocket(ip, port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Tagger.Client(self.protocol)
        self.open()

    def open(self):
        return self.transport.open()

    def basic_struct(self, content):
        return self.client.basic_struct(content)

    def tag(self, text, mode):
        return self.client.tag(text, mode)

    def close(self):
        return self.transport.close()

    def client(self):
        return self.client()



def start_html(d):
    res_str = ""
    res_str += '<!DOCTYPE html>\r\n<html lang="zh-CN">' + "\r\n"
    res_str += '<style> .possymp{border:1px solid #00f;color:#a00;font-size:13px;font-weight:bold;padding:2px 2px 2px 2px;} </style>' + "\r\n"
    res_str += '<style> .negsymp{border:1px solid #00f;color:#a00;font-size:13px;font-weight:bold;padding:2px 2px 2px 2px;text-decoration:line-through;} </style>' + "\r\n"
    res_str += '<style> .title1{color:#0a0;font-size:18px;font-weight:bold;} </style>' + "\r\n"
    res_str += '<style> .title2{font-size:16px;font-weight:bold;} </style>' + "\r\n"
    res_str += '<head>\r\n<meta charset="utf-8">\r\n<meta http-equiv="X-UA-Compatible" content="IE=edge">\r\n<meta name="viewport" content="width=device-width, initial-scale=1">\r\n<title>bingli-%s</title>\r\n<link href="/bootstrap/css/bootstrap.min.css" rel="stylesheet">\r\n<script src="/bootstrap/js/jquery.min.js"></script>\r\n<script src="/bootstrap/js/bootstrap.min.js"></script>\r\n<script src="//cdn.bootcss.com/html5shiv/3.7.2/html5shiv.min.js"></script>\r\n<script src="//cdn.bootcss.com/respond.js/1.4.2/respond.min.js"></script>\r\n</head>\r\n<body>' % d + "\r\n"
    res_str += '<div style="width:800px;border:1px solid #000;padding:10px 10px 10px 10px;">' + "\r\n"
    return res_str

def end_html():
    res_str = ""
    res_str += '</div>'
    res_str += "</body>\r\n</html>"
    return res_str

def title_1(u_text):
    return '<div class="title1">%s</div>' % u_text

def title_2(u_text):
    return '<div class="title2">%s</div>' % u_text

def norm_text(u_text):
    return '<div>%s</div>' % u_text

def writeFile(filename, content):
    with open(filename, "w") as f:
        f.write(content)

class TimeCal():
    def __init__(self):
        self.begin = time.time()

    def reset(self):
        self.begin = time.time()

    def cost(self):
        return time.time() - self.begin
def tagCaseHtml(ip, port, filename, content, outpath):
    res_json_dict = {}
    res_json_dict["symp_text"] = ""
    all_pos_tag = set()
    all_neg_tag = set()
    all_polarity_res = {}
    all_range_lower = {}
    all_range_upper = {}
    all_kv_res = {}

    #rpc_client = getRpcClient(tagger_host)
    rpc_client = TaggerClient(ip, port)

    timecal = TimeCal()
    try:
        bs = rpc_client.basic_struct(content)
    except:
        print traceback.format_exc()
        print "%s:%d deal with %s failed" %(ip, port, filename), 
        print timecal.cost()
        rpc_client.close()
        return

    res_ret = start_html(filename)
    """
    case html format
    1: simple text
    2: complex text
    """
    caseHtmlMap =  OrderedDict()
    caseHtmlMap[u"基本信息"] = [
            ("name", u"姓名", 1),
            ("gender", u"性别", 1),
            ("age", u"患病年龄", 1),
            ("status", u"当前状态", 1),
            ("diagnosis_date", u"确诊时间",1),
            ("treat_date", u"治疗时间", 1),
            ("treat_hospital", u"治疗医院", 1),
            ("doctor_comment", u"医生评价", 1),
            ("hospital_comment", u"医院评价", 1)
        ]
    caseHtmlMap[u"治疗方案"] = [
            ("surgery", u"手术", 2),
            ("radiotherapy", u"放疗", 1),
            ("chemotherapy", u"化疗", 1),
            ("medicine", u"成药", 1),
            ("herbal", u"中草药", 1),
        ]
    caseHtmlMap[u"入院记录"] = [
            ("complain", u"主诉", 2),
            ("sympton", u"主要症状", 2),
            ("med_his", u"现病史", 2),
            ("person_his", u"个人史", 1),
            ("family_his", u"家庭史", 1),
            ("med_exam", u"医学检查", 2),
            ("body_exam", u"体格检查", 2),
            ("spec_exam", u"专科检查", 2),
            ("acce_exam", u"辅助检查", 1),
        ]
    caseHtmlMap[u"出院记录"] =  [
            ("med_exp", u"入院情况及诊疗经过", 2),
            ("effect", u"出院情况及治疗效果", 2),
            ("diagnosis", u"出院诊断", 2),
            ("advice", u"出院医嘱", 1),
            ("days", u"住院天数", 1),
        ]
    for p in caseHtmlMap:
        res_ret += title_1(p)
        for row in caseHtmlMap[p]:
            title = row[0]
            name =row[1]
            type_ = row[2]
            if title in bs:
                if type_ == 1:
                    #simple text
                    res_ret += title_2(name)
                    res_ret += norm_text(bs[title])
                elif type_ == 2:
                    res_ret += title_2(name)
                    timecal.reset()
                    try:
                        
                        tag_res  = rpc_client.tag(bs[title], "doc")
                    except:
                        print traceback.format_exc()
                        print "%s:%d deal with %s failed" %(ip, port, filename), timecal.cost()
                        rpc_client.close()
                        return
                    all_pos_tag = all_pos_tag | set(tag_res.pos_tag)
                    all_neg_tag = all_neg_tag | set(tag_res.neg_tag)
                    for k in tag_res.polarity_res:
                        all_polarity_res[k] = tag_res.polarity_res[k]
                    for k in tag_res.range_res_lower:
                        all_range_lower[k] = tag_res.range_res_lower[k]
                    for k in tag_res.range_res_upper:
                        all_range_upper[k] = tag_res.range_res_upper[k]
                    for k in tag_res.kv_value:
                        all_kv_res[k] = tag_res.kv_value[k]
                    res_json_dict["symp_text"] += bs[title] + "\r\n"
                    res_ret += norm_text(tag_res.mk_str)
    rpc_client.close()
    res_ret += end_html()

    res_json_dict["symp_pos_tag"] = list(all_pos_tag)
    res_json_dict["symp_neg_tag"] = list(all_neg_tag)
    for key in all_polarity_res:
        res_json_dict[key] = all_polarity_res[key]
    for key in all_range_lower:
        res_json_dict[key] = all_range_lower[key]
    for key in all_range_upper:
        res_json_dict[key] = all_range_upper[key]
    for key in all_kv_res:
        res_json_dict[key] = all_kv_res[key]
    res_json = json.dumps(res_json_dict)
    try:
        js = json.loads(res_json.encode('utf8'))
    except:
        print s, path
        js = json.loads(s)
    li = []
    for tag in js["symp_pos_tag"]:
        li.append(tag)
    js["symp_pos_tag"] = li
    li = []
    for tag in js["symp_neg_tag"]:
        li.append(tag)
    js["symp_neg_tag"] = li
    js["symp_text"] = js["symp_text"].strip()
    for key in all_polarity_res:
        js[key] = all_polarity_res[key]
    for key in all_range_lower:
        js[key] = all_range_lower[key]
    for key in all_range_upper:
        js[key] = all_range_upper[key]
    for key in all_kv_res:
        js[key] = all_kv_res[key]

    out_file = os.path.join(outpath, filename.split(".")[0] + ".html")
    writeFile(out_file, res_ret)

    id = filename.split('.')[0]
    try:
        #es.indexWapper(int(id), js)
        key = {"_id":int(id)}
        mongo_client = Mongo(host=mongo_host, port=mongo_port, db=mongo_db, table=mongo_table)
        mongo_client.update(key, js)
        #mongo_client.close()
    except:
        print id, js, traceback.format_exc()
        return


    print out_file

def wapper(args):
    return tagCaseHtml(*args)

if __name__ == "__main__":

    config = Config("../conf/build.conf")

    base = config.get("path", "input")
    if base[-1] != '/':
        base += '/'
    outpath = config.get("path", "output")
    if outpath[-1] != '/':
        outpath += '/'

    mongo_host = config.get("mongo", "host")
    mongo_port = int(config.get("mongo", "port"))
    mongo_db = config.get("mongo", "db")
    mongo_table = config.get("mongo", "table")

    tagger_host = config.get("tagger", "host")
    tagger_timeout = int(config.get("tagger", "timeout"))
    tagger_mode = config.get("tagger", "mode")

    #es = ESIndex(es_host, es_batch, es_type)
    cases = []
    for d in os.listdir(base):
        file_name = os.path.join(base, d)
        content = open(file_name).read()
        host = tagger_host[random.choice(xrange(0, len(tagger_host)))]
        ip = tagger_host.split(':')[0]
        port  = tagger_host.split(':')[-1]
        cases.append([ip, int(port), d, content, outpath])
        #tagCaseHtml(ip, int(port), d, content, outpath)

    #from gevent.pool import Pool
    pool = Pool(6)
    result = pool.map(wapper, cases)
    #pool.close()
    #pool.join()

