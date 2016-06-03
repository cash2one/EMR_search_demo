# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import json

class EMRPreproc:
    def __init__(self):
        self.messy_code = {}

        self.latin_replace = {}
        self.latin_replace[u". "] = u"。"
        self.latin_replace[u"，"] = u","
        self.latin_replace[u"："] = u":"
        self.latin_replace[u"；"] = u";"
        self.latin_replace[u"？"] = u"?"
        self.latin_replace[u"！"] = u"!"
        self.latin_replace[u"（"] = u"("
        self.latin_replace[u"）"] = u")"
        
        self.yx_title_dict = {}

    def load_messy_code(self, file_name):
        for line in open(file_name):
            self.messy_code[eval(line.rstrip("\r\n"))] = 1
        
    def load_yx_title(self, file_name):
        fp = open(file_name)
        title_dict = {}
        for line in fp:
            f = line.rstrip("\r\n").split("\t")
            if len(f) != 2:
                print "Error: yx title dict format error", line.rstrp("\r\n")
                return {}
            title_dict[f[0].decode("utf8")] = f[1]

        self.yx_title_dict = title_dict
        
    def calc_disp_width(self, u_text):
        width = 0
        for u in u_text:
            if u <= u"\u024f":
                width += 0.5
            else:
                width += 1
                
        return width

    def proc_messy(self, u_text):
        #for k in self.latin_replace:
        #    u_text = u_text.replace(k, self.latin_replace[k])

        clean_text = u""
        accum_line = u""
        for line in u_text.split(u"\n"):
            line = line.rstrip(u"\r\n")
            clean_line = u""
            for i in xrange(len(line)):
                if line[i] in self.messy_code:
                    if i == len(line) - 1:
                        clean_line += u":"
                    else:
                        clean_line += u","
                else:
                    clean_line += line[i]
            if clean_line in self.yx_title_dict:
                if accum_line != u"":
                    clean_text += accum_line + u"\r\n"
                clean_text += clean_line + u"\r\n"
                accum_line = ""
                continue
            if self.calc_disp_width(line) < 30 or clean_line[-1] in [u"。", u"?", u"!", u"？", u"！"]:
                accum_line += clean_line + u"\r\n"
            else:
                accum_line += clean_line

        if accum_line != u"":
            clean_text += accum_line + u"\r\n"

        return clean_text

    def basic_struct(self, u_text):
        ret_struct = {}
        curr_tag = None
        for line in u_text.split(u"\n"):
            norm_line = line.rstrip(u"\r\n").replace(u"：", u":")
            if norm_line in self.yx_title_dict:
                new_tag = self.yx_title_dict[norm_line]
                if new_tag == "#":
                    continue
                tag = new_tag
                ret_struct[tag] = ""
                curr_tag = tag
                continue
            if curr_tag != None:
                ret_struct[tag] += line.rstrip(u"\r\n") + u"\r\n"

        return ret_struct

def proc_file(file_name):
    content = open(file_name).read().decode("utf8")
    print json.dumps(emr_preproc.basic_struct(content), encoding='UTF-8', ensure_ascii=False)

if __name__ == "__main__":
    emr_preproc = EMRPreproc()
    emr_preproc.load_yx_title("yx_seg_title.txt")
    emr_preproc.load_messy_code("messy_code.txt")
    base = sys.argv[1]
    if os.path.isdir(base):
        for d in os.listdir(base):
            file_name = os.path.join(base, d)
            proc_file(file_name)
    else:
        proc_file(base)
