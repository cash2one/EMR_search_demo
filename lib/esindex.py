#encoding=utf8
# -*- coding: utf-8 -*-
import sys
reload(sys)

import json
import commands
from elasticsearch import Elasticsearch, exceptions, helpers

class ESIndex:
    def __init__(self, hosts, index = "", doc_type = ""):
        self.es = Elasticsearch(hosts)
        self.index = index
        self.doc_type = doc_type

    def index(self, doc_id, body, index = "", doc_type = ""):
        index_ = self.index if index == "" else index
        doc_type_ = self.doc_type if doc_type == "" else doc_type
        return self.es.index(index=index_, doc_type=doc_type_, body=body, id=doc_id)

    def delete(self,doc_id, index = "", doc_type = ""):
        index_ = self.index if index == "" else index
        doc_type_ = self.doc_type if doc_type == "" else doc_type
        return self.es.delete(index=index_, doc_type = doc_type_, id = doc_id)
        
    def bulk(self, docs, index = "", doc_type = "", op_type = 'index'):
        '''
        bulk sample:
        {"_op_type":"index", _index" : "test", "_type" : "type1", "_id" : "1" , "_source":{"field1":"value1", "field2":"value2"}}
        { "_op_type":"delete" ,  "_index" : "test", "_type" : "type1", "_id" : "2" } 

        '''
        index_ = self.index if index == "" else index
        doc_type_ = self.doc_type if doc_type == "" else doc_type
 
        allow_op = ['index', 'delete']
        if op_type not in allow_op:
            raise exceptions.RequestError(400, '{"msg":"op_type is not allowed, you can use index or delete"}')

        actions = []
        for doc in docs:
            action = {}
            action["_index"] = index_
            action["_type"] = doc_type_
            action["_id"] = doc["_id"]
            if op_type == 'index':
                del doc["_id"]
                action["_source"] = doc
            action["_op_type"] = op_type
            actions.append(action)

        return helpers.parallel_bulk(self.es, actions)

    def getDoc(self,doc_id, index = "", doc_type = ""):
        index_ = self.index if index == "" else index
        doc_type_ = self.doc_type if doc_type == "" else doc_type
 
        return self.es.get(index=index_, doc_type=doc_type_, id=doc_id)

    def putMapping(self, body, index = "", doc_type =""):
        index_ = self.index if index == "" else index
        doc_type_ = self.doc_type if doc_type == "" else doc_type
        return self.es.indices.put_mapping(index=index_, doc_type=doc_type_, body=body)

    def create(self, body = {}, index = "", timeout = 30):
        index_ = self.index if index == "" else index
        return self.es.indices.create(index_, body=body)
         
if __name__ == "__main__":
    es = ESIndex("127.0.0.1:9200", "20160606", "case")
    print json.dumps(es.getDoc('29824'))



