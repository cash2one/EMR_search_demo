#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

import sys, glob
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../mining/entity_tag/src/")
sys.path.append("../lib/")
sys.path.append('gen-py')

import traceback
from entity_tag import *
from entity_dict import *
from emr_preprocessor import EMRPreproc
from config import Config

from tag import Tagger

from tag.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.protocol import TCompactProtocol 
from thrift.server import TServer
from thrift.server import TProcessPoolServer
import json
from ForkedPdb import ForkedPdb, pdb
import multiprocessing
from jpype import *
import time
import logging
logging.basicConfig()

class TagHandler:
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
        print "taghandler"

    def check(self, path):
        if not os.path.exists(path):
            raise IOError(-1, 'not exist', path)


    def basic_struct(self, text):
        print multiprocessing.current_process().name, "calling basic_struct"
        try:
            res  = self.emr_preproc.basic_struct(text)
        except:
            err = traceback.format_exc()
            print err
            return {"msg":err}
        return res

    def tag(self, text, mode):
        tagres = tagResult()
        #ForkedPdb().set_trace()
        begin = time.time()
        tagres.pos_tag, tagres.neg_tag, tagres.polarity_res,tagres.range_res_lower,\
        tagres.range_res_upper, tagres.kv_value, tagres.mk_str  = self.tagger.tag(text, mode)
        print multiprocessing.current_process().name, "calling tag, cost ", time.time() - begin
        return tagres

def wapper(port):
    """
    entity_tag use hanlp with jpype, jvm in jpype existed in every process can work well
    """
    handler = TagHandler('../conf/entity_tag.conf')
    processor = Tagger.Processor(handler)
    transport = TSocket.TServerSocket(port=port)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    #pfactory = TCompactProtocol.TCompactProtocolFactory()
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    server.serve()

    
if __name__ == "__main__":
    #startJvm()
    '''
    handler = TagHandler('../conf/entity_tag.conf')
    processor = Tagger.Processor(handler)
    transport = TSocket.TServerSocket(port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    #server = TServer.TForkingServer(processor, transport, tfactory, pfactory)
    server = TProcessPoolServer.TProcessPoolServer(processor, transport, tfactory, pfactory)
    server.setPostForkCallback(startJvm)
    #server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    #server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    #server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

    print 'Starting the server...'
    server.serve()
    print 'done.'
    '''

    pool_size = 8
    pool = multiprocessing.Pool(pool_size)
    ips = []
    for i in xrange(0, pool_size):
        ips.append(i+9090)
    pool.map(wapper, ips)
    print "finished"
 
