# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("/home/cihang/word-seg/src")
from entity_dict import *
from text_feature import *
from word_seg import *
from jpype import *
import os
from bs4 import BeautifulSoup
from parse_yx import *

class EPhrase():
    def __init__(self):
        self.text = None
        self.tags = []

class ESection():
    def __init__(self):
        self.phrases = []

    def add(self, x):
        self.phrases.append(x)

class ESentence():
    def __init__(self):
        self.sections = []

    def add(self, x):
        self.sections.append(x)

class EntityTagger():
    def __init__(self, edict):
        self.edict = edict
        self.max_len = 0
        for w in self.edict.words:
            if len(w) > self.max_len:
                self.max_len = len(w)
        self.fp = None
        self.ws = WordSeg()
        self.feature = TextFeature()
        startJVM(getDefaultJVMPath(), "-Djava.class.path=/home/cihang/HanLP/hanlp.jar:/home/cihang/HanLP")
        self.dp = JClass("com.hankcs.hanlp.dependency.CRFDependencyParser")

    def word_seg(self, u_str):
        stop_words = [u",", u".", u":", u";", u"!", u"?", u"，", u"。", u"：", u"；" , u"！", u"？", u"、", u"的", u"了", u" "]
        terms = self.ws.seg_word(u_str.encode("gbk"))
        clean_terms = []
        for t in terms:
            ut = t.decode("gbk")
            if ut not in stop_words:
                clean_terms.append(ut)

        return clean_terms

    def match_max(self, u_str, u_dict):
        for i in xrange(0, len(u_str)):
            if u_str[0:(len(u_str)-i)] in u_dict:
                return u_str[0:(len(u_str)-i)]

        return None

    def forward_max_matching(self, u_str):
        ret_list = []
        last_phrase = u""
        while True:
            max_seg_len = self.max_len
            if len(u_str) < self.max_len:
                max_seg_len = len(u_str)

            match_str = self.match_max(u_str[0:max_seg_len], self.edict.words)
            if match_str == None:
                match_len = 1
                last_phrase += u_str[0]
            else:
                if last_phrase != u"":
                    ret_list.append(last_phrase)
                    last_phrase = u""
                match_len = len(match_str)
                ret_list.append(match_str)
            if len(u_str) - match_len <= 0:
                if last_phrase != u"":
                    ret_list.append(last_phrase)
                    last_phrase = u""
                return ret_list
            u_str = u_str[match_len:]

    def exact_tag_sen(self, u_str):
        f_sec = u_str.replace(u"，", u",").replace(u"：", u",").replace(u"；", u",").replace(u":", u",").replace(u";", u",").split(u",")
        pos_tag = {}
        neg_tag = {}
        for sec in f_sec:
            if sec.lstrip("\r\n\t ").rstrip("\r\n\t ") != u"":
                phrase_list = self.forward_max_matching(sec)
                neg = False
                for p in phrase_list:
                    if (p.find(u"无") != -1 or p.find(u"未见") != -1 or p.find(u"没有") != -1) and p.find(u"诱因") == -1:
                        neg = True
                    if self.fp != None:
                        self.fp.write(p)
                    if p in self.edict.ridx:
                        for e in self.edict.ridx[p]:
                            if self.fp != None:
                                if not neg:
                                    print >> self.fp, '<span class="possymp">&nbsp;%s&nbsp;</span>' % e.entity_name,
                                if neg:
                                    print >> self.fp, '<span class="negsymp">&nbsp;%s&nbsp;</span>' % e.entity_name,
                            if not neg:
                                pos_tag[e.entity_name] = 1
                            if neg:
                                neg_tag[e.entity_name] = 1
            if self.fp != None:
                print >> self.fp, "，",

        return (pos_tag, neg_tag)

    def find_pos(self, u_str, u_c):
        pos = []
        last_pos = u_str.find(u_c)
        while last_pos != -1:
            pos.append(last_pos)
            last_pos = u_str.find(u_c, last_pos + 1)

        return pos

    def check_inverse(self, query, doc, entity):
        hit_w = []
        if len(query) <= 1:
            return 0

        for w in query:
            if w in doc:
                hit_w.append(w)
        
        w_pair = {}
        for i in xrange(len(hit_w) - 1):
            for j in xrange(i+1, len(hit_w)):
                w_pair[(hit_w[i], hit_w[j])] = 0

        for pair in w_pair:
            total_num = 0.0
            inverse_num = 0.0
            for word in entity.entrance_word:
                first_pos = self.find_pos(word, pair[0])
                second_pos = self.find_pos(word, pair[1])
                if first_pos == [] or second_pos == []:
                    continue
                for i in first_pos:
                    for j in second_pos:
                        total_num += 1
                        if i > j:
                            inverse_num += 1
            w_pair[pair] = inverse_num / total_num

        f = doc.replace(u"，", u",").replace(u"、", u",").replace(u"；", u",").replace(u"；", u",").split(u",")
        inverse_detected = False
        for pair in w_pair:
            if w_pair[pair] > 0.01:
                continue
            first_pos = []
            second_pos = []
            for (i, s) in enumerate(f):
                if s.find(pair[0]) != -1:
                    first_pos.append(i)
                if s.find(pair[1]) != -1:
                    second_pos.append(i)
            order_num = 0
            for i in first_pos:
                for j in second_pos:
                    if i <= j:
                        order_num += 1

            if order_num == 0:
                inverse_detected = True
                break

        if inverse_detected:
            return 1
        else:
            return 0

    def tag_sen_basic(self, u_str):
        f = u_str.replace(u"，", u",").replace(u"：", u",").replace(u"；", u",").replace(u":", u",").replace(u";", u",").split(u",")

        pos_tag = {}
        neg_tag = {}
        for e in self.edict.entities:
            cqr = []
            last_sec_with_n = []
            neg = False
            for u_sec in f:
                sf = u_sec.replace(u"、", u",").split(u",")
                for u_pha in sf:
                    if u_pha.lstrip("\r\n\t ").rstrip("\r\n\t ") == u"":
                        continue
                    doc_terms = set(u_pha)
                    cqr_entrance = []
                    for word in e.entrance_word:
                        hit_num = 0.0
                        for t in word:
                            if t in doc_terms:
                                hit_num += 1
                        cqr_entrance.append(hit_num / len(word))
                    cqr_sort = sorted(cqr_entrance)
                    if len(cqr) == 0 or cqr_sort[-1] > max(cqr):
                        if (u_sec.find(u"无") != -1 or u_sec.find(u"未见") != -1 or u_sec.find(u"没有") != -1) and u_sec.find(u"诱因") == -1:
                            neg = True      
                        else:
                            neg = False
                    cqr.append(cqr_sort[-1])
            cqr_sort = sorted(cqr)
            if cqr_sort[-1] > 0.9:
                if not neg:
                    pos_tag[e.entity_name] = cqr_sort[-1]
                if neg:
                    neg_tag[e.entity_name] = cqr_sort[-1]
                    
        return (pos_tag, neg_tag)

    def tag_sen_bisec(self, u_str):
        f = u_str.replace(u"，", u",").replace(u"：", u",").replace(u"；", u",").replace(u":", u",").replace(u";", u",").split(u",")
        ff = []
        for u_sec in f:
            sf = u_sec.replace(u"、", u",").split(u",")
            if (u_sec.find(u"无") != -1 or u_sec.find(u"未见") != -1 or u_sec.find(u"没有") != -1) and u_sec.find(u"诱因") == -1:
                neg = True
            else:
                neg = False
            for u_pha in sf:
                ff.append((u_pha, neg))

        bi_sec = []
        if len(f) == 1:
            return ({}, {})
        else:
            for i in xrange(len(ff) - 1):
                bi_sec.append((ff[i][0] + u"," + ff[i+1][0], ff[i+1][1]))

        pos_tag = {}
        neg_tag = {}
        for e in self.edict.entities:
            cqr = []
            last_sec_with_n = []
            neg = False
            for (u_sec, sec_neg) in bi_sec:
                if u_sec.lstrip("\r\n\t ").rstrip("\r\n\t ") == u"":
                    continue
                doc_terms = set(u_sec)
                cqr_entrance = []
                for word in e.entrance_word:
                    hit_num = 0.0
                    for t in word:
                        if t in doc_terms:
                            hit_num += 1
                    inverse_rate = self.check_inverse(word, u_sec, e)
                    if inverse_rate < 0.01:
                        cqr_entrance.append(hit_num / len(word))
                    else:
                        cqr_entrance.append(0)
                cqr_sort = sorted(cqr_entrance)
                if len(cqr) == 0 or cqr_sort[-1] > max(cqr):
                    neg = sec_neg
                cqr.append(cqr_sort[-1])
            cqr_sort = sorted(cqr)
            if cqr_sort[-1] > 0.9:
                if not neg:
                    pos_tag[e.entity_name] = cqr_sort[-1]
                if neg:
                    neg_tag[e.entity_name] = cqr_sort[-1]

        return (pos_tag, neg_tag)

    def tag_sen_dp(self, u_str):
        f = u_str.replace(u"，", u",").replace(u"：", u",").replace(u"；", u",").replace(u":", u",").replace(u";", u",").split(u",")
        ff = []
        for u_sec in f:
            sf = u_sec.replace(u"、", u",").split(u",")
            if (u_sec.find(u"无") != -1 or u_sec.find(u"未见") != -1 or u_sec.find(u"没有") != -1) and u_sec.find(u"诱因") == -1:
                neg = True
            else:
                neg = False
            for u_pha in sf:
                ff.append((u_pha, neg))

        f = u_str.replace(u"，", u",").replace(u"、", u",").replace(u"；", u",").replace(u"；", u",").split(u",")

        pos_tag = {}
        neg_tag = {}
        for e in self.edict.entities:
            cqr = []
            last_sec_with_n = None
            neg = False
            for (i, (u_sec, sec_neg)) in enumerate(ff):
                if u_sec.lstrip("\r\n\t ").rstrip("\r\n\t ") == u"":
                    continue

                dp_result = self.dp.compute(u_sec.encode("utf8")).getWordArray()
                core_tag = None
                for s in dp_result:
                    if s.toString().split()[7] == u"核心成分":
                        core_tag = s.toString().split()[4]
                if ((core_tag != "n" and core_tag != None) or len(dp_result) == 1)and last_sec_with_n != None:
                    u_sec += "," + last_sec_with_n
                if (core_tag == "n" and len(dp_result) != 1) or i == 0:
                    last_sec_with_n = u_sec

                doc_terms = set(u_sec)

                cqr_entrance = []
                for word in e.entrance_word:
                    hit_num = 0.0
                    for t in word:
                        if t in doc_terms:
                            hit_num += 1
                    inverse_rate = self.check_inverse(word, u_sec, e)
                    if inverse_rate < 0.01:
                        cqr_entrance.append(hit_num / len(word))
                    else:
                        cqr_entrance.append(0)
                cqr_sort = sorted(cqr_entrance)
                if len(cqr) == 0 or cqr_sort[-1] > max(cqr):
                    neg = sec_neg
                cqr.append(cqr_sort[-1])
            cqr_sort = sorted(cqr)
            if cqr_sort[-1] > 0.9:
                if not neg:
                    pos_tag[e.entity_name] = cqr_sort[-1]
                if neg:
                    neg_tag[e.entity_name] = cqr_sort[-1]

        return (pos_tag, neg_tag)

    def tag_sen_bisec_ld(self, u_str):
        f = u_str.replace(u"，", u",").split(u",")

        pos_tag = {}
        neg_tag = {}
        last_sec = ""
        for e in self.edict.entities:
            cqr = []
            last_sec_with_n = []
            for u_sec in f:
                if u_sec.lstrip("\r\n\t ").rstrip("\r\n\t ") == u"":
                    continue
                if (u_sec.find(u"无") != -1 or u_sec.find(u"未见") != -1 or u_sec.find(u"没有") != -1) and u_sec.find(u"诱因") == -1:
                    neg = True
                else:
                    neg = False
                sf = u_str.split(u"、")
                
                if len(sf) <= 1 or u_sec == None:
                    last_sec = u_sec
                    continue
                for u_des in sf:
                    doc_terms = set(u_des + last_sec)
                    cqr_entrance = []
                    for word in e.entrance_word:
                        hit_num = 0.0
                        for t in word:
                            if t in doc_terms:
                                hit_num += 1
                        inverse_rate = self.check_inverse(word, u_sec + "," + last_sec, e)
                        if inverse_rate < 0.01:
                            cqr_entrance.append(hit_num / len(word))
                        else:
                            cqr_entrance.append(0)
                    cqr_sort = sorted(cqr_entrance)
                    cqr.append(cqr_sort[-1])
                cqr_sort = sorted(cqr)
                if cqr_sort[-1] > 0.9:
                    if not neg:
                        pos_tag[e.entity_name] = cqr_sort[-1]
                    if neg:
                        neg_tag[e.entity_name] = cqr_sort[-1]
                last_sec = sf[0]

        return (pos_tag, neg_tag)

    def fuzzy_tag_sen(self, u_str):
        all_tags = []
        all_tags.append(self.tag_sen_basic(u_str))
        all_tags.append(self.tag_sen_bisec(u_str))
        all_tags.append(self.tag_sen_dp(u_str))
        all_tags.append(self.tag_sen_bisec_ld(u_str))

        all_pos_tag = {}
        all_neg_tag = {}
        for (pos_tag, neg_tag) in all_tags:
            for t in pos_tag:
                if pos_tag[t] > 0.9 and t not in all_neg_tag:
                    all_pos_tag[t] = pos_tag[t]
            for t in neg_tag:
                if neg_tag[t] > 0.9 and t not in all_pos_tag:
                    all_neg_tag[t] = neg_tag[t]

        return (all_pos_tag, all_neg_tag)

    def tag(self, u_str, output_file = ""):
        if output_file != "":
            self.fp = open(output_file, "w")
            print >> self.fp, '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
            print >> self.fp, '<html>'
            print >> self.fp, '<style> .possymp{border:2px solid #00f;color:#00a;font-size:13px;font-weight:bold;padding:2px 2px 2px 2px;} </style>'
            print >> self.fp, '<style> .negsymp{border:2px solid #00f;color:#00a;font-size:13px;font-weight:bold;padding:2px 2px 2px 2px;text-decoration:line-through;} </style>'
            print >> self.fp, '<body>'
        elif self.fp != None:
            self.fp.close()
            self.fp = None
        f_sen = u_str.rstrip(u"\r\n\t ").lstrip("\r\n\t ").split(u"。")
        pos_tag = set()
        neg_tag = set()
        for sen in f_sen:
            if sen.lstrip("\r\n\t ").rstrip("\r\n\t ") == u"":
                continue
            (exact_pos_tag, exact_neg_tag) = self.exact_tag_sen(sen)
            (fuzzy_pos_tag, fuzzy_neg_tag) = self.fuzzy_tag_sen(sen)
            pos_tag.update(exact_pos_tag.keys())
            neg_tag.update(exact_neg_tag.keys())
            for t in fuzzy_pos_tag:
                if t not in exact_neg_tag:
                    pos_tag.add(t)
                    if self.fp != None and t not in exact_pos_tag:
                        print >> self.fp, '<span class="possymp">&nbsp;%s&nbsp;</span>' % t,
            for t in fuzzy_neg_tag:
                if t not in exact_pos_tag:
                    neg_tag.add(t)
                    if self.fp != None and t not in exact_neg_tag:
                        print >> self.fp, '<span class="negsymp">&nbsp;%s&nbsp;</span>' % t,
            print >> self.fp, "。"
        if self.fp != None:
            print >> self.fp, "</body>\r\n</html>"
            self.fp.close()
            self.fp = None

        return (pos_tag, neg_tag)
                
if __name__ == "__main__":
    edict = EntityDict("symp")
    edict.load_file("../data/zhichangai_symp.csv")
    etagger = EntityTagger(edict)
    #etagger.tag(u"3月余前起无明显诱因下出现大便习惯改变，大便次数增多，约5-8次/天，初大便稀烂，黄色，无粘液、血便，间中有腹痛，下腹部明显，多为隐痛，无向他处放射，到当医院中医就诊予以对症治疗后（具体不详）症状无明显好转。半月余前到就诊，行肠镜检查考虑直肠癌（报告未回）。今为进一步治疗拟“直肠癌”收入我科。起病以来，无发热、盗汗、咳嗽、咳痰、肛门停止排气排便、呕吐、身目黄染。精神、睡眠均佳，食欲良好，大便", "test.html")
    if not os.path.isdir(sys.argv[1]):
        file_name = sys.argv[1]
        bs = BeautifulSoup(open(file_name))
        bingli_node = bs.body.find_all(name="ul", class_="datailCon")
        lis = bingli_node[0].find_all(name="li")
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
            etagger.tag(his, sys.argv[2])
        exit(0)

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
            etagger.tag(his, os.path.join(sys.argv[2], d))
            
