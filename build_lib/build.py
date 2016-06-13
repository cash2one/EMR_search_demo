#encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../lib/")
import json
import os
import zerorpc
from multiprocessing import Pool
from config import Config
import traceback
from collections import OrderedDict
from esindex import ESIndex
import random

global es

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

def tagCaseHtml(tagger_host, filename, content, outpath):
    res_json_dict = {}
    res_json_dict["symp_text"] = ""
    all_pos_tag = set()
    all_neg_tag = set()
    all_polarity_res = {}
    all_range_lower = {}
    all_range_upper = {}
    all_kv_res = {}

    rpc_client = zerorpc.Client()
    host = tagger_host[random.choice(xrange(0, len(tagger_host)))]
    rpc_client.connect("tcp://%s" %(host))
    try:
        bs = rpc_client.basic_struct(content)
    except:
        print traceback.format_exc()
        print "%s deal with %s failed" %(host, filename)
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
                    try:
                        (pos_tag, neg_tag, polarity_res, range_lower, range_upper, kv_res, mk_str) = rpc_client.tag(bs[title], "doc")
                    except:
                        print traceback.format_exc()
                    all_pos_tag = all_pos_tag | set(pos_tag)
                    all_neg_tag = all_neg_tag | set(neg_tag)
                    for k in polarity_res:
                        all_polarity_res[k] = polarity_res[k]
                    for k in range_lower:
                        all_range_lower[k] = range_lower[k]
                    for k in range_upper:
                        all_range_upper[k] = range_upper[k]
                    for k in kv_res:
                        all_kv_res[k] = kv_res[k]
                    res_json_dict["symp_text"] += bs[title] + "\r\n"
                    res_ret += norm_text(mk_str)
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
    es.indexWapper(int(id), js)


    print out_file

def wapper(args):
    return tagCaseHtml(*args)

if __name__ == "__main__":

    config = Config("./build.conf")

    base = config.get("path", "input")
    if base[-1] != '/':
        base += '/'
    outpath = config.get("path", "output")
    if outpath[-1] != '/':
        outpath += '/'

    es_host = config.get("index", "host")
    es_batch = config.get("index", "batch")
    es_type = config.get("index", "type")

    tagger_host = config.get("tagger", "host").split(";")
    tagger_timeout = int(config.get("tagger", "timeout"))
    tagger_mode = config.get("tagger", "mode")

    es = ESIndex(es_host, es_batch, es_type)

    cases = []
    for d in os.listdir(base):
        file_name = os.path.join(base, d)
        content = open(file_name).read().decode("utf8")
        cases.append([tagger_host, d, content, outpath])
        #tagCaseHtml(d, content, outpath)

    from gevent.pool import Pool
    pool = Pool(3)
    result = pool.map(wapper, cases)
    pool.join()

