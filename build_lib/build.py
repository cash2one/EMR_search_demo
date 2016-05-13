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

if __name__ == "__main__":
    edict = EntityDict("symp")
    edict.load_file("../mining/entity_tag/data/zhichangai_symp.csv")
    patternList = Pattern().getPattern()
    etagger = EntityTagger(edict, patternList, "/home/yongsheng/EMR_search_demo/mining/entity_tag/dict/wordseg_dict/")

    base = sys.argv[1]
    batch = sys.argv[3]

    post = 'curl -XPOST http://localhost:9200/' + batch + '/case/'

    for d in os.listdir(base):
        file_name = os.path.join(base, d)
        bs = BeautifulSoup(open(file_name))
        if bs.body == None:
            continue
        bingli_node = bs.body.find_all(name="ul", class_="datailCon")
        if len(bingli_node) == 0:
            continue
        lis = bingli_node[0].find_all(name="li")
        if len(lis) == 0:
            continue
        disease = ""
        symp = []
        his = ""
        check = ""
        for li in lis:
            key = li.span.string
            if key == u"所患疾病：":
                disease = parse_disease(li.p)
                #print disease
            elif key == u"主要症状：":
                symp = parse_symp(li.p)
                #print symp
            elif key == u"现在病史：":
                his = parse_his(li.p)
                #print his
            elif key == u"医学检查：":
                check = parse_check(li.p)
        text = his.lstrip(u"\r\n\t ").rstrip(u"\r\n\t ") + u"。" + check.lstrip(u"\r\n\t ").rstrip(u"\r\n\t ")
        if text != None and text.lstrip(u"\r\n\t ").rstrip(u"\r\n\t ") != u"":
            ret_tag = etagger.tag(text, "")
            res_json_dict = {}
            (pos_tag, neg_tag, polarity_res) = etagger.tag(text, os.path.join(sys.argv[2], d))
            res_json_dict["symp_pos_tag"] = list(pos_tag)
            res_json_dict["symp_neg_tag"] = list(neg_tag)
            res_json_dict["symp_text"] = text
            for key in polarity_res:
                res_json_dict[key] = polarity_res[key]
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
            for key in polarity_res:
                js[key] = polarity_res[key]

            id = d.split('.html')[0]
            cmd = post + id + " -d \'%s\'" %(json.dumps(js))
            print commands.getstatusoutput(cmd)

