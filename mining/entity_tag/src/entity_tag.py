# -*- coding: utf-8 -*-
import sys
import re
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
from pattern import * 

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
    def __init__(self, edict, epattern, ws_dict_path = "", mode = "doc"):
        self.edict = edict
        self.epattern = epattern
        self.max_len = 0
        for w in self.edict.words:
            if len(w) > self.max_len:
                self.max_len = len(w)
        #if ws_dict_path == "":
        #    self.ws = WordSeg()
        #else:
        #    self.ws = WordSeg(dict_path = ws_dict_path)
        self.feature = TextFeature()
        startJVM(getDefaultJVMPath(), "-Djava.class.path=/home/cihang/HanLP/hanlp.jar:/home/cihang/HanLP")
        self.dp = JClass("com.hankcs.hanlp.dependency.CRFDependencyParser")
        self.mode = mode

        self.mk_str = ""

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
        if self.mode == "query":
            f_sec = u_str.replace(u"，", u",").replace(u"：", u",").replace(u"；", u",").replace(u":", u",").replace(u";", u",").replace(u" ", u",").split(u",")
        else:
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
                    self.mk_str += p
                    if p in self.edict.ridx:
                        for e in self.edict.ridx[p]:
                            if not neg:
                                self.mk_str += '<span class="possymp">&nbsp;%s&nbsp;</span>' % e.entity_name
                            if neg:
                                self.mk_str += '<span class="negsymp">&nbsp;%s&nbsp;</span>' % e.entity_name
                            if not neg:
                                pos_tag[e.entity_name] = 1
                            if neg:
                                neg_tag[e.entity_name] = 1
            self.mk_str += "，"

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
        if self.mode == "query":
            f = u_str.replace(u"，", u",").replace(u"：", u",").replace(u"；", u",").replace(u":", u",").replace(u";", u",").replace(u" ", u",").split(u",")
        else:
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
            if len(cqr_sort) > 0 and cqr_sort[-1] > 0.9:
                if not neg:
                    pos_tag[e.entity_name] = cqr_sort[-1]
                if neg:
                    neg_tag[e.entity_name] = cqr_sort[-1]
                    
        return (pos_tag, neg_tag)

    def tag_sen_bisec(self, u_str):
        if self.mode == "query":
            f = u_str.replace(u"，", u",").replace(u"：", u",").replace(u"；", u",").replace(u":", u",").replace(u";", u",").replace(u" ", u",").split(u",")
        else:
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
            if len(cqr_sort) > 0 and cqr_sort[-1] > 0.9:
                if not neg:
                    pos_tag[e.entity_name] = cqr_sort[-1]
                if neg:
                    neg_tag[e.entity_name] = cqr_sort[-1]

        return (pos_tag, neg_tag)

    def tag_sen_dp(self, u_str):
        if self.mode == "query":
            f = u_str.replace(u"，", u",").replace(u"：", u",").replace(u"；", u",").replace(u":", u",").replace(u";", u",").replace(u" ", u",").split(u",")
        else:
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
        dp_dict = {}
        for e in self.edict.entities:
            cqr = []
            last_sec_with_n = None
            neg = False
            for (i, (u_sec, sec_neg)) in enumerate(ff):
                if u_sec.lstrip("\r\n\t ").rstrip("\r\n\t ") == u"":
                    continue

                if u_sec in dp_dict:
                    dp_result = dp_dict[u_sec]
                else:
                    dp_result = self.dp.compute(u_sec.encode("utf8")).getWordArray()
                    dp_dict[u_sec] = dp_result
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
            if len(cqr) > 0 and cqr_sort[-1] > 0.9:
                if not neg:
                    pos_tag[e.entity_name] = cqr_sort[-1]
                if neg:
                    neg_tag[e.entity_name] = cqr_sort[-1]

        return (pos_tag, neg_tag)

    def tag_sen_bisec_ld(self, u_str):
        if self.mode == "query":
            f = u_str.replace(u"，", u",").replace(u" ", u",").split(u",")
        else:
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
                if len(cqr_sort) > 0 and cqr_sort[-1] > 0.9:
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

    def get_min_segment(self, pattern, line, seperator):
        line = line.strip()
        L = line.split(seperator)
        Index = []

        for i in range(len(L)):
            for ele in L[i]:
                Index.append(i)
            if i != len(L) - 1:
                Index.append(i)
       
        searchObj = re.search(pattern, line)
        if not searchObj:
            return ["", ""]
        segment = searchObj.group()
        begin = Index[line.find(segment)]
        end = Index[line.find(segment) + len(segment) -1]
        newL = []
        i = end
        while i >= begin:
            newline = seperator.join(L[i:end+1])
            searchObj = re.search(pattern, newline)
            if searchObj:
                return [newline, searchObj]
            i -= 1
        return [seperator.join(L[begin:end+1]), searchObj]

    def get_range_value(self, u_str):
        Res_lower = {}
        Res_upper = {}
        for pattern in self.epattern:
            if pattern.type_ != "R":
                 continue
            tag_range = self.get_min_segment(pattern.range_pattern, u_str, "，")
            if tag_range[1] != "":
                Res_lower[pattern.name] = tag_range[1].group(1)
                Res_upper[pattern.name] = tag_range[1].group(2)
                
        return Res_lower, Res_upper 

    def get_point_value(self, u_str):
        Res = {}
        Value = {}
        for pattern in self.epattern:
            if pattern.type_ != "KV":
                 continue
            tag_kv = self.get_min_segment(pattern.range_pattern, u_str, "，")
            if tag_kv[1] != "":
                #print tag_kv[1].group()
                #print tag_kv[1].group(0)
                #print tag_kv[1].group(1)
                #print tag_kv[1].group(2)
                #print tag_kv[1].group(3)
                s = ""
                Res[pattern.name] = tag_kv[1].group(0)
                if pattern.digital_index != -1:
                    s = tag_kv[1].group(pattern.digital_index)
                if s != "":
                    Value[pattern.name] = float(s)

        return Res, Value
   
    def get_multi_value(self, u_str):
        Res = {}
        Value = {}
        for pattern in self.epattern:
            if pattern.type_ != "KVS":
                continue
            tag_kv = self.get_min_segment(pattern.regex, u_str, "，")
            if tag_kv[1] != "":
                s = ""
                Res[pattern.name] = tag_kv[1].group(0)
                Value[pattern.name] = []
                if pattern.digital_index1 != -1:
                    s = tag_kv[1].group(pattern.digital_index1)
                if s != "":
                    s = s.replace("^", "e")
                    Value[pattern.name].append(float(s))
                if pattern.digital_index2 != -1:
                    s = tag_kv[1].group(pattern.digital_index2)
                if s != "":
                    s = s.replace("^", "e")
                    Value[pattern.name].append(float(s))
                    
        return Res, Value
    
    def get_polarity_value(self, u_str):
        Res = {}
        for pattern in self.epattern:
            if pattern.type_ != "P":
                 continue
            tag_yang = self.get_min_segment(pattern.yang, u_str, "，")[0]
            tag_ying = self.get_min_segment(pattern.ying, u_str, "，")[0]
            if tag_yang == "" and tag_ying == "":
                Res[pattern.name] = ""
                continue
            if len(tag_yang) > 0 and tag_ying == "":
                Res[pattern.name] = "阳"
                continue
            if len(tag_ying) > 0 and tag_yang == "":
                Res[pattern.name] = "阴"
                continue
            if len(tag_ying) < len(tag_yang):
                Res[pattern.name] = "阴"
            else:
                Res[pattern.name] = "阳"
        return Res

    def tag(self, u_str):
        self.mk_str = ""

        f_sen = u_str.rstrip(u"\r\n\t ").lstrip("\r\n\t ").split(u"。")
        pos_tag = set()
        neg_tag = set()
        polarity_res = {}
        range_res_lower = {}
        range_res_upper = {}
        kv_res = {}
        kv_value = {}
        kvs_res = {}
        kvs_value = {}
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
                    if t not in exact_pos_tag:
                        self.mk_str += '<span class="possymp">&nbsp;%s&nbsp;</span>' % t
            for t in fuzzy_neg_tag:
                if t not in exact_pos_tag:
                    neg_tag.add(t)
                    if t not in exact_neg_tag:
                        self.mk_str += '<span class="negsymp">&nbsp;%s&nbsp;</span>' % t

            res = self.get_polarity_value(sen)
            for key in res:
                if res[key] != "":
                    polarity_res[key] = res[key]    
                if res[key] != "":
                    self.mk_str += '<span class="possymp">&nbsp;%s%s&nbsp;</span>' % (key, res[key])

            [res_lower, res_upper] = self.get_range_value(sen)
            for key in res_lower:
                if res_lower[key] != "":
                    range_res_lower[key] = res_lower[key]
                    range_res_upper[key] = res_upper[key]
                if res_lower[key] != "" and res_upper[key] != "":
                    t="-"
                    self.mk_str += '<span class="possymp">&nbsp;%s%s%s%s&nbsp;</span>' % (key, res_lower[key],t,res_upper[key])
          
            [res, value] = self.get_point_value(sen)
            for key in res:
                if res[key] != "":
                    kv_res[key] = res[key]
                if key in value:
                    kv_value[key] = value[key]
                if res[key] != "":
                    self.mk_str += '<span class="possymp">&nbsp;%s%s&nbsp;</span>' % (key, res[key])

            [res, value] = self.get_multi_value(sen)
            for key in res:
                if res[key] != "":
                    kvs_res[key] = res[key]
                if key in value:
                    kvs_value[key] = value[key]
                if res[key] != "":
                    self.mk_str += '<span class="possymp">&nbsp;%s%s&nbsp;</span>' % (key, res[key])


            self.mk_str += "。"

        return (pos_tag, neg_tag, polarity_res, range_res_lower, range_res_upper, kv_res, kvs_res, self.mk_str)
                
if __name__ == "__main__":
    edict = EntityDict("symp")
    edict.load_file("../data/zhichangai_symp.csv")
    patternList = Pattern().getPattern()
    etagger = EntityTagger(edict, patternList)
    for pattern in etagger.epattern:
        print pattern.name
        print pattern.type_


    s = u"血常规、尿常规无异常，大便潜血（+）"
    s = u"血常规、尿常规无异常，大便潜血（+），梅毒+HIV（-）"
    s = u"血常规、尿常规无异常，大便潜血（+），梅毒HIV（-）"
    s = u"血常规、尿常规无异常，大便潜血(-)，梅毒+HIV（-）"
    s = u"一次，为鲜红色，于大便相混，无粘液、脓性分泌物，偶有头晕，休息后缓解，未予重视，两年前因“胸闷、心悸到当地医院就诊，入院查大便常规发现潜血阳性，后复查潜血阴性，诊断为“1.上消化道出血 2.左肾石症”，予以护胃、改善循环治疗并予出院"
    s = u"血常规：Hb103g/L，WBC6.83×109/L，PLT268×109/L。大便潜血可疑阳性，大便常规正常。尿常规正常。"
    s = u"大便潜血可疑阳性，大便常规正常"
    s = u"3月余前起无明显诱因下出现大便习惯改变，大便潜血（+），大便次数增多，约5-8次/天，初大便稀烂，黄色，无粘液、血便，间中有腹痛，下腹部明显，多为隐痛，无向他处放射，到当医院中医就诊予以对症治疗后（具体不详）症状无明显好转。半月余前到就诊，行肠镜检查考虑直肠癌（报告未回）。今为进一步治疗拟“直肠癌”收入我科。起病以来，无发热、盗汗、咳嗽、咳痰、肛门停止排气排便、呕吐、身目黄染。精神、睡眠均佳，食欲良好，大便潜血(+)，梅毒+HIV（-）"
    s = "大便潜血阳性"
    s = u"血常规：Hb103g/L，WBC6.83×109/L，PLT268×109/L。大便潜血可疑阳性，大便常规正常。尿常规正常。CA19-9 12.34U/ml"
    s = u"[2010-01-16]查血常规，HGB65g/L胃镜未见明显异常 2、[2010-01-16]血常规，WBC 8.41×10^9/L，HB 65g/L，生化组合示，钠，133mmol/L，钙，1.87mmol/L， 肝功能，ALB，25.7g/L， 2010-01-16，电子胃镜，食管、胃及十二指肠未见异常"
    s = u"血常规,WBC 14.35 x 10^9/L,NEU 0.735"
    s = u"WBC 8.41×10^9/L"
    s = u"(carbohydrate antigen,CA)19-9为187,68 U,ml,血清甲胎蛋白(α-fetoprotein,AFP)为3484,61 ng,ml,血清癌胚抗原为6,25 ng,ml。"
    s = u"血清糖链抗原(carbohydrate antigen,CA)19-9为187,68 U,ml,血清甲胎蛋白(α-fetoprotein,AFP)为3484,61 ng,ml,血清癌胚抗原为6,25 ng,ml。"

    (a,b,c,d,e,f,g,h) = etagger.tag(s)
    for ele in c:
        print ele, c[ele]
    for ele in d:
        print ele, d[ele]
    for ele in e:
        print ele, e[ele]
    print "len(c)", len(f)
    print "len(d)", len(f)
    print "len(e)", len(f)
    print "len(f)", len(f)
    print "len(g)", len(f)
    for ele in f:
        print "f",ele, f[ele]
    for ele in g:
        print "g",ele, g[ele]
    exit(0)

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
        text = his.lstrip(u"\r\n\t ").rstrip(u"\r\n\t ") + u"。" + check.lstrip(u"\r\n\t ").rstrip(u"\r\n\t ")
        #if his != None and his.lstrip(u"\r\n\t ").rstrip(u"\r\n\t ") != u"":
        #    etagger.tag(his, sys.argv[2])
        #if check != None and check.lstrip(u"\r\n\t ").rstrip(u"\r\n\t ") != u"":
        #    etagger.tag(check, sys.argv[2])
        if text != None and text.lstrip(u"\r\n\t ").rstrip(u"\r\n\t ") != u"":
            (a,b,c) = etagger.tag(text, sys.argv[2])
            for ele in c:
                print ele, c[ele]
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
            
