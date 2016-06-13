#encoding=utf8
# -*- coding: utf-8 -*-
import sys
reload(sys)

import json
import commands
from elasticsearch import Elasticsearch, exceptions, helpers

class ESIndex:
    def __init__(self, hosts, index, doc_type):
        self.es = Elasticsearch(hosts)
        self._index = index
        self._doc_type = doc_type

    def indexWapper(self, doc_id, body): 
        return self.es.index(index=self._index, doc_type=self._doc_type, body=body, id=doc_id)

    def index(self, index, doc_type, doc_id, body):
        return self.es.index(index=index, doc_type=doc_type, body=body, id=doc_id)

    def deleteWapper(self, doc_id):
        return self.es.delete(index=self._index, doc_type = self._doc_type, id = doc_id)

    def delete(self, index, doc_type, doc_id):
        return self.es.delete(index=index, doc_type = doc_type, id = doc_id)
        
    def bulk(self, index, doc_type, docs, op_type = 'index'):
        '''
        bulk sample:
        {"_op_type":"index", _index" : "test", "_type" : "type1", "_id" : "1" , "_source":{"field1":"value1", "field2":"value2"}}
        { "_op_type":"delete" ,  "_index" : "test", "_type" : "type1", "_id" : "2" } 

        '''
        allow_op = ['index', 'delete']
        if op_type not in allow_op:
            raise exceptions.RequestError(400, '{"msg":"op_type is not allowed, you can use index or delete"}')

        actions = []
        for doc_id in docs:
            action = {}
            action["_index"] = index
            action["_type"] = doc_type
            action["_id"] = doc_id
            if op_type == 'index':
                action["_source"] = docs[doc_id]
            action["_op_type"] = op_type
            actions.append(action)

        return helpers.parallel_bulk(self.es, actions)

    def getDoc(self,index, doc_type, doc_id):
        return self.es.get(index=index, doc_type=doc_type, id=doc_id)

    def getDocWapper(self, doc_id):
        return self.es.get(index=self._index, doc_type=self._doc_type, id=doc_id)

if __name__ == "__main__":
    es = ESIndex("127.0.0.1:9200", "20160606", "case")
    print json.dumps(es.getDoc('29824'))



