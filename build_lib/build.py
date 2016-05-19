#encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../mining/entity_tag/src/")
import os
import json
import commands
from entity_tag import *
from entity_dict import *
from emr_preprocessor import EMRPreproc
from pool import MultiPool
import traceback

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

def doTask( etagger, batch, emr_preproc, bs, filename, outpath):
    res_json_dict = {}
    res_json_dict["symp_text"] = ""
    all_pos_tag = set()
    all_neg_tag = set()
    all_polarity_res = {}
    all_range_lower = {}
    all_range_upper = {}
    all_kv_res = {}

    res_ret = start_html(filename)

    res_ret += title_1(u"基本信息")
    if "name" in bs:
        res_ret += title_2(u"姓名")
        res_ret += norm_text(bs["name"])

    if "gender" in bs:
        res_ret += title_2(u"性别")
        res_ret += norm_text(bs["gender"])

    if "age" in bs:
        res_ret += title_2(u"患病年龄")
        res_ret += norm_text(bs["age"])

    if "status" in bs:
        res_ret += title_2(u"当前状态")
        res_ret += norm_text(bs["status"])

    if "diagnosis_date" in bs:
        res_ret += title_2(u"确诊时间")
        res_ret += norm_text(bs["diagnosis_date"])

    if "treat_date" in bs:
        res_ret += title_2(u"治疗时间")
        res_ret += norm_text(bs["treat_date"])

    if "treat_hospital" in bs:
        res_ret += title_2(u"治疗医院")
        res_ret += norm_text(bs["treat_hospital"])

    if "doctor_comment" in bs:
        res_ret += title_2(u"医生评价")
        res_ret += norm_text(bs["doctor_comment"])

    if "hospital_comment" in bs:
        res_ret += title_2(u"医院评价")
        res_ret += norm_text(bs["hospital_comment"])

    res_ret += title_1(u"治疗方案")
    if "surgery" in bs:
        res_ret += title_2(u"手术")
        (pos_tag, neg_tag, polarity_res, range_lower, range_upper, kv_res, mk_str) = etagger.tag(bs["surgery"])
        all_pos_tag = all_pos_tag | pos_tag
        all_neg_tag = all_neg_tag | neg_tag
        for k in polarity_res:
            all_polarity_res[k] = polarity_res[k]
        for k in range_lower:
            all_range_lower[k] = range_lower[k]
        for k in range_upper:
            all_range_upper[k] = range_upper[k]
        for k in kv_res:
            all_kv_res[k] = kv_res[k]
        res_json_dict["symp_text"] += bs["surgery"] + "\r\n"
        res_ret += norm_text(mk_str)

    if "radiotherapy" in bs:
        res_ret += title_2(u"放疗")
        res_ret += norm_text(bs["radiotherapy"])

    if "chemotherapy" in bs:
        res_ret += title_2(u"化疗")
        res_ret += norm_text(bs["chemotherapy"])

    if "medicine" in bs:
        res_ret += title_2(u"成药")
        res_ret += norm_text(bs["medcine"])

    if "herbal" in bs:
        res_ret += title_2(u"中草药")
        res_ret += norm_text(bs["herbal"])

    res_ret += title_1(u"入院记录")
    if "complain" in bs:
        res_ret += title_2(u"主诉")
        (pos_tag, neg_tag, polarity_res, range_lower, range_upper, kv_res, mk_str) = etagger.tag(bs["complain"])
        all_pos_tag = all_pos_tag | pos_tag
        all_neg_tag = all_neg_tag | neg_tag
        for k in polarity_res:
            all_polarity_res[k] = polarity_res[k]
        for k in range_lower:
            all_range_lower[k] = range_lower[k]
        for k in range_upper:
            all_range_upper[k] = range_upper[k]
        for k in kv_res:
            all_kv_res[k] = kv[res]
        res_json_dict["symp_text"] += bs["complain"] + "\r\n"
        res_ret += norm_text(mk_str)

    if "sympton" in bs:
        res_ret += title_2(u"主要症状")
        (pos_tag, neg_tag, polarity_res, range_lower, range_upper, kv_res, mk_str) = etagger.tag(bs["sympton"])
        all_pos_tag = all_pos_tag | pos_tag
        all_neg_tag = all_neg_tag | neg_tag
        for k in polarity_res:
            all_polarity_res[k] = polarity_res[k]
        for k in range_lower:
            all_range_lower[k] = range_lower[k]
        for k in range_upper:
            all_range_upper[k] = range_upper[k]
        for k in kv_res:
            all_kv_res[k] = kv[res]
        res_json_dict["symp_text"] += bs["sympton"] + "\r\n"
        res_ret += norm_text(mk_str)

    if "med_his" in bs:
        res_ret += title_2(u"现病史")
        (pos_tag, neg_tag, polarity_res, range_lower, range_upper, kv_res, mk_str) = etagger.tag(bs["med_his"])
        all_pos_tag = all_pos_tag | pos_tag
        all_neg_tag = all_neg_tag | neg_tag
        for k in polarity_res:
            all_polarity_res[k] = polarity_res[k]
        for k in range_lower:
            all_range_lower[k] = range_lower[k]
        for k in range_upper:
            all_range_upper[k] = range_upper[k]
        for k in kv_res:
            all_kv_res[k] = kv[res]
        res_json_dict["symp_text"] += bs["med_his"] + "\r\n"
        res_ret += norm_text(mk_str)

    if "person_his" in bs:
        res_ret += title_2(u"个人史")
        res_ret += norm_text(bs["person_his"])
        
    if "family_his" in bs:
        res_ret += title_2(u"家庭史")
        res_ret += norm_text(bs["family_his"])

    if "med_exam" in bs:
        res_ret += title_2(u"医学检查")
        (pos_tag, neg_tag, polarity_res, range_lower, range_upper, kv_res, mk_str) = etagger.tag(bs["med_exam"])
        all_pos_tag = all_pos_tag | pos_tag
        all_neg_tag = all_neg_tag | neg_tag
        for k in polarity_res:
            all_polarity_res[k] = polarity_res[k]
        for k in range_lower:
            all_range_lower[k] = range_lower[k]
        for k in range_upper:
            all_range_upper[k] = range_upper[k]
        for k in kv_res:
            all_kv_res[k] = kv_res[k]
        res_json_dict["symp_text"] += bs["med_exam"] + "\r\n"
        res_ret += norm_text(mk_str)

    if "body_exam" in bs:
        res_ret += title_2(u"体格检查")
        (pos_tag, neg_tag, polarity_res, range_lower, range_upper, kv_res, mk_str) = etagger.tag(bs["body_exam"])
        all_pos_tag = all_pos_tag | pos_tag
        all_neg_tag = all_neg_tag | neg_tag
        for k in polarity_res:
            all_polarity_res[k] = polarity_res[k]
        for k in range_lower:
            all_range_lower[k] = range_lower[k]
        for k in range_upper:
            all_range_upper[k] = range_upper[k]
        for k in kv_res:
            all_kv_res[k] = kv_res[k]
        res_json_dict["symp_text"] += bs["body_exam"] + "\r\n"
        res_ret += norm_text(mk_str)

    if "spec_exam" in bs:
        res_ret += title_2(u"专科检查")
        (pos_tag, neg_tag, polarity_res, range_lower, range_upper, kv_res, mk_str) = etagger.tag(bs["spec_exam"])
        all_pos_tag = all_pos_tag | pos_tag
        all_neg_tag = all_neg_tag | neg_tag
        for k in polarity_res:
            all_polarity_res[k] = polarity_res[k]
        for k in range_lower:
            all_range_lower[k] = range_lower[k]
        for k in range_upper:
            all_range_upper[k] = range_upper[k]
        for k in kv_res:
            all_kv_res[k] = kv_res[k]
        res_json_dict["symp_text"] += bs["spec_exam"] + "\r\n"
        res_ret += norm_text(mk_str)

    if "acce_exam" in bs:
        res_ret += title_2(u"辅助检查")
        res_ret += norm_text(bs["acce_exam"])

    res_ret += title_1(u"出院记录")
    if "med_exp" in bs:
        res_ret += title_2(u"入院情况及诊疗经过")
        (pos_tag, neg_tag, polarity_res, range_lower, range_upper, kv_res, mk_str) = etagger.tag(bs["med_exp"])
        all_pos_tag = all_pos_tag | pos_tag
        all_neg_tag = all_neg_tag | neg_tag
        for k in polarity_res:
            all_polarity_res[k] = polarity_res[k]
        for k in range_lower:
            all_range_lower[k] = range_lower[k]
        for k in range_upper:
            all_range_upper[k] = range_upper[k]
        for k in kv_res:
            all_kv_res[k] = kv_res[k]
        res_json_dict["symp_text"] += bs["med_exp"] + "\r\n"
        res_ret += norm_text(mk_str)
    
    if "effect" in bs:
        res_ret += title_2(u"出院情况及治疗效果")
        (pos_tag, neg_tag, polarity_res, range_lower, range_upper, kv_res, mk_str) = etagger.tag(bs["effect"])
        all_pos_tag = all_pos_tag | pos_tag
        all_neg_tag = all_neg_tag | neg_tag
        for k in polarity_res:
            all_polarity_res[k] = polarity_res[k]
        for k in range_lower:
            all_range_lower[k] = range_lower[k]
        for k in range_upper:
            all_range_upper[k] = range_upper[k]
        for k in kv_res:
            all_kv_res[k] = kv_res[k]
        res_json_dict["symp_text"] += bs["effect"] + "\r\n"
        res_ret += norm_text(mk_str)

    if "diagnosis" in bs:
        res_ret += title_2(u"出院诊断")
        (pos_tag, neg_tag, polarity_res, range_lower, range_upper, kv_res, mk_str) = etagger.tag(bs["diagnosis"])
        all_pos_tag = all_pos_tag | pos_tag
        all_neg_tag = all_neg_tag | neg_tag
        for k in polarity_res:
            all_polarity_res[k] = polarity_res[k]
        for k in range_lower:
            all_range_lower[k] = range_lower[k]
        for k in range_upper:
            all_range_upper[k] = range_upper[k]
        for k in kv_res:
            all_kv_res[k] = kv_res[k]
        res_json_dict["symp_text"] += bs["diagnosis"] + "\r\n"
        res_ret += norm_text(mk_str)
        
    if "advice" in bs:
        res_ret += title_2(u"出院医嘱")
        res_ret += norm_text(bs["advice"])

    if "days" in bs:
        res_ret += title_2(u"住院天数")
        res_ret += norm_text(bs["days"])

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
    out_fp = open(out_file, "w")
    print >> out_fp, res_ret
    out_fp.close()

    post = 'curl -XPOST http://localhost:9200/' + batch + '/case/'
    id = filename.split('.')[0]
    cmd = post + id + " -d \'%s\'" %(json.dumps(js))
    print commands.getstatusoutput(cmd)

def taskProcesser(params):
    edict = EntityDict("symp")
    #edict.load_file("../mining/entity_tag/data/zhichangai_symp.csv")
    edict.load_file("../mining/entity_tag/data/class_term.dict.gbk")
    patternList = Pattern().getPattern()
    etagger = EntityTagger(edict, patternList, "../mining/entity_tag/dict/wordseg_dict/")
    for batch, emr_preproc, bs, d, outpath in params:
        try:
            doTask(etagger, batch, emr_preproc, bs, d, outpath)
        except:
            print traceback.format_exc()


if __name__ == "__main__":
    thread_num = 6

    base = sys.argv[1]
    outpath = sys.argv[2]
    batch = sys.argv[3]

    '''
    etaggers = []
    for i in range(0, thread_num):
        etagger = EntityTagger(edict, patternList, "../mining/entity_tag/dict/wordseg_dict/")
        etaggers.append(etagger)
    '''
    emr_preproc = EMRPreproc()
    emr_preproc.load_yx_title("../mining/entity_tag/data/yx_seg_title.txt")
    emr_preproc.load_messy_code("../mining/entity_tag/data/messy_code.txt")

    pool = MultiPool(thread_num)
    taskParams = {} 
    i = 0
    for d in os.listdir(base):
        file_name = os.path.join(base, d)
        content = open(file_name).read().decode("utf8")
        bs = emr_preproc.basic_struct(content)
        #doTask(etagger, batch, emr_preproc, bs, d, sys.argv[2])
        #pool.add_job(doTask, etaggers[i%thread_num], batch, emr_preproc, bs, d, sys.argv[2])
        index = i % thread_num
        if index not in taskParams:
            taskParams[index] = []
        taskParams[index].append((batch, emr_preproc, bs, d, outpath))
        i = i+1

    for i in range(0, thread_num):
        pool.addJob(taskProcesser, taskParams[i])
    pool.waitClose()





