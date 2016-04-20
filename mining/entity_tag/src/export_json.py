# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from entity_tag import *
from entity_dict import *

if __name__ == "__main__":
    edict = EntityDict("symp")
    edict.load_file("../data/zhichangai_symp.csv")
    etagger = EntityTagger(edict)

    for d in os.listdir(sys.argv[1]):
        file_name = os.path.join(sys.argv[1], d)
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
        if his != None and his.lstrip(u"\r\n\t ").rstrip(u"\r\n\t ") != u"":
            ret_tag = etagger.tag(his, "")
            res_json_dict = {}
            ret_tag = etagger.tag(his, os.path.join(sys.argv[2], d))
            res_json_dict["symp_tag"] = list(ret_tag)
            res_json_dict["symp_text"] = his
            res_json = json.dumps(res_json_dict)
            output_fp = open(os.path.join(sys.argv[2], d), "w")
            print >> output_fp, res_json
            
            
