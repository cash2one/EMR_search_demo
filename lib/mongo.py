#encoding=utf8
from pymongo import MongoClient

class Mongo:
    def __init__(self, host="localhost", port=27017, db="db", table=""):
        self.client = MongoClient(host, port)
        self.db = self.client[db]
        self.table = table

    def bulk(self, datalist, table = ""):
        table_ = self.table if table == "" else table
        return self.db[table_].insert_many(datalist)

    def insert(self, data, table = ""):
        table_ = self.table if table == "" else table
        return self.db[table_].insert_one(data)

    def find(self, table = "", filter_= {}):
        table_ = self.table if table == "" else table
        return self.db[table_].find(filter_)
    def findOne(self, table = "", filter_ = {}):
        table_ = self.table if table == "" else table
        return self.db[table_].find_one(filter_)

    def delete(self, table = "", filter_ = {}):
        table_ = self.table if table == "" else table
        return self.db[table_].delete_many(filter_)

    def update(self, key, value, table = "", insert=True):
        table_ = self.table if table == "" else table
        return self.db[table_].update(key, value, upsert=insert)

    def size(self, table = ""):
        table_ = self.table if table == "" else table
        return self.db[table_].count()

    def drop(self, table = ""):
        table_ = self.table if table == "" else table
        return self.db[table_].drop()


if __name__ == "__main__":
    mongo = Mongo(db="algorithm", host="192.168.1.100")
    print mongo.delete("tag").deleted_count
    '''
    datas = [
    {"_id":124, "name":"lucy", "age":20},
    {"_id":124, "name":"monkey", "age":20}]
    print mongo.bulk('tag', datas)
    '''
    #key = {'_id':125}
    #value = {"$set":{"name":"fuck"}}
    #print mongo.update('tag', key, value)
