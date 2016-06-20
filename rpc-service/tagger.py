#encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../mining/entity_tag/src/")
sys.path.append("../webserver/")
import json
import os
import zerorpc
from entity_tag import *
from entity_dict import *
from emr_preprocessor import EMRPreproc
import traceback
import gevent
import time
from config import Config
from multiprocessing import Pool

class Tagger(object):
    def __init__(self, conf):
        config = Config(conf)
        yx_title = config.get("emr_preproc", "yx_title")
        messy_code = config.get("emr_preproc", "messy_code")
        dict_type = config.get("entity_dict", "dict_type")
        dict_file = config.get("entity_dict", "dict_file")
        jianyan = config.get("pattern", "jianyan")
        wordseg_dict = config.get("entity_dict", "wordseg_dict")
        javapath = config.get("hanlp", "javapath")
        class_ = config.get("hanlp", "class")
        ####
        self.check(yx_title)
        self.check(messy_code)
        self.check(dict_file)
        self.check(jianyan)
        self.check(wordseg_dict)
        self.check(javapath)
        ###
        self.emr_preproc = EMRPreproc()
        self.emr_preproc.load_yx_title(yx_title)
        self.emr_preproc.load_messy_code(messy_code)

        edict = EntityDict(dict_type)
        edict.load_file(dict_file)

        patternList = Pattern(jianyan).getPattern()

        self.tagger = EntityTagger(edict, patternList, javapath, class_, wordseg_dict)

    def check(self, path):
        if not os.path.exists(path):
            raise IOError(-1, 'not exist', path)

    def tag(self, txt, mode):
        print 'calling tag '
        return self.tagger.tag(txt, mode)

    def basic_struct(self, content):
        print 'calling basic_struct'
        return self.emr_preproc.basic_struct(content)

def wapper(ip):
    conf = '../conf/entity_tag.conf'
    server = zerorpc.Server(Tagger(conf))
    server.bind("tcp://0.0.0.0:%d" %(ip))
    server.run()
    server.close()


if __name__ == "__main__":
    pool_size = 6
    #server = zerorpc.Server(Tagger(), pool_size = pool_size)
    #server = zerorpc.Server(Tagger(conf))
    #server.bind("tcp://0.0.0.0:9999")
    print 'tagger service start....'
   # server.run()
   # server.close()

    pool = Pool(pool_size)
    ips = []
    for i in xrange(0, pool_size):
        ips.append(i+9990)
    pool.map(wapper, ips)
 

