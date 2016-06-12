#encoding=utf8
# -*- coding: utf-8 -*-
import sys
reload(sys)

import json
import commands
from elasticsearch import Elasticsearch

class ESSearch:
    def __init__(self, hosts, tagfunc):
        self.es = Elasticsearch(hosts)
        self.tagfunc = tagfunc

    def tag(self, *args):
        return self.tagfunc(*args)

    def queryBuilder(self, keywords, indicatorRange = {}):
        """
        @input keywords
        @output query in json
        """
        #sample
        '''
        query = {
            "form":0,
            "size":10,
            "query":{
                "bool":{
                    "must": { "match": {"symp_tag":must}},
                    "must_not": {"match": {"symp_text": must_not}},
                    "should": [
                        {"match":{"symp_text":should_1}},
                        {"match":{"symp_text":should_2}}
                    ]
                }
            }
        }
        '''
        (pos_tag, neg_tag, polarity_res, range_lower, range_upper, kv_res, mk_str) = self.tag(keywords, 'query')

        print "keywords", keywords
        print "pos tag", u" ".join(list(pos_tag))
        print "neg tag", u" ".join(list(neg_tag))
        for key in polarity_res:
            print "search.py", key + "\t" + polarity_res[key]

        query_dict = {}
        query_dict["query"] = {}
        query_dict["query"]["bool"] = {}
        match_text = {}
        match_text["match_phrase"] = {}
        match_text["match_phrase"]["symp_text"] = {}
        match_text["match_phrase"]["symp_text"]["query"] = keywords
        match_text["match_phrase"]["symp_text"]["slop"] = 2
        polarity_flag = True
        for key in polarity_res:
            if polarity_res != "":
                polarity_falg = False
        if len(pos_tag) == 0 and len(neg_tag) == 0 and polarity_flag:
            query_dict["query"]["bool"]["must"] = match_text
        else:
            query_dict["query"]["bool"]["should"] = []
            #query_dict["query"]["bool"]["should"].append(match_text)
            query_dict["query"]["bool"]["should"].append({})
            tag_bool_query = query_dict["query"]["bool"]["should"][-1]
            tag_bool_query["bool"] = {}
            tag_bool_query["bool"]["must"] = []
            for tag in pos_tag:
                tag_bool_query["bool"]["must"].append({})
                s = tag_bool_query["bool"]["must"][-1]
                s["match"] = {}
                s["match"]["symp_pos_tag"] = tag.encode("utf8")
            for tag in neg_tag:
                tag_bool_query["bool"]["must"].append({})
                s = tag_bool_query["bool"]["must"][-1]
                s["match"] = {}
                s["match"]["symp_neg_tag"] = tag.encode("utf8")
            for key in polarity_res:
                if polarity_res[key] == "":
                    continue
                print "search.py polarity_res[key]", len(polarity_res[key])
                tag_bool_query["bool"]["must"].append({})
                s = tag_bool_query["bool"]["must"][-1]
                s["match"] = {}
                s["match"][key] = polarity_res[key].encode("utf8")
        ranges = {}
        for indicator in indicatorRange:
            sub = {}
            sub['from'] = float(indicatorRange[indicator][0])
            sub['to'] = float(indicatorRange[indicator][1])
            ranges[indicator] = sub
        if len(ranges) > 0:
            query_dict["query"]["bool"]["filter"] = {'range':ranges}

        print json.dumps(query_dict)
        return query_dict

    def processResult(self, res):
        return res['hits']

    def search(self, keywords, indicatorRange, index, doc_type, start = 0, size = 10):
        #indicatorRange
        #{'血常规':['1.2', '2.4'], ...}
        query = self.queryBuilder(keywords, indicatorRange)
        response = self.es.search(index=index, doc_type = doc_type, body=query, from_ = start, size = size)
        return self.processResult(response)

   
if __name__ == "__main__":
    import zerorpc
    client = zerorpc.Client()
    client.connect("tcp://192.168.1.100:9999")
    es = ESSearch("127.0.0.1:9200", client.tag)
    print es.tag("便血", 'query')
    client.close()
