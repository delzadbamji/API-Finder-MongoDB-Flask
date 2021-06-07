import random

import pymongo
import bson
from bson.json_util import dumps
from tqdm import tqdm
import re

uri = "env.URI"

client = pymongo.MongoClient(uri, connectTimeoutMS=200, retryWrites=True)
print(client)
print(client.list_database_names())
pa3 = client.pa3
apidb = pa3['apidb']
mashupdb = pa3['mashupdb']

def query_results(input,apitype):

    title,rating,ratingdrop,updated,updateddrop,protocol,tag,category,summary,description,APIname,label = input
    # print(title,rating,ratingdrop,updated,updateddrop,protocol,tag,category)
    result = []
    for i in tqdm(range(5), ncols=80,smoothing=0, unit=" Query-Retrieval-Rate"):
        pass
    print("entered the mongo_query simulation....")

    current_db = apidb if apitype == "API" else mashupdb

    if title!="":
        cursor = current_db.find({"title":{ "$regex": re.compile(title, re.IGNORECASE)}},{"title":1,"id":1,"_id":0,"name":1})
        result.append(dumps(cursor))
    if rating!="":
        if ratingdrop=="eq":
            cursor = current_db.find({"rating":rating}, {"rating": 1, "id": 1, "_id": 0,"name":1})
            result.append(dumps(cursor))
        elif ratingdrop=="gt":
            # print("entered")
            pipeline = [{"$match":{"rating":{"$gt":rating,"$ne":""}}},{"$project":{"id":1,"rating":1,"_id":0,"name":1}}]
            cursor = current_db.aggregate(pipeline)
            # print(dumps(cursor, indent=2))
            result.append(dumps(cursor))
        else: #lt
            pipeline = [{"$match": {"rating": {"$lt":rating,"$ne":""}}}, {"$project": {"id": 1, "rating": 1, "_id": 0,"name":1}}]
            cursor = current_db.aggregate(pipeline)
            # print(dumps(cursor, indent=2))
            result.append(dumps(cursor))

    if updated!="":
        if updateddrop=="eq":
            cursor = current_db.find({"updated":updated}, {"updated": 1, "id": 1, "_id": 0,"name":1})
            result.append(dumps(cursor))

        elif updateddrop=="gt":
            # print("entered")
            pipeline = [{"$match":{"updated":{"$gt":updated,"$ne":""}}},{"$project":{"id":1,"updated":1,"_id":0,"name":1}}]
            cursor = current_db.aggregate(pipeline)
            # print(dumps(cursor, indent=2))
            result.append(dumps(cursor))
        else: #lt
            pipeline = [{"$match": {"updated": {"$lt":updated,"$ne":""}}}, {"$project": {"id": 1, "updated": 1, "_id": 0,"name":1}}]
            cursor = current_db.aggregate(pipeline)
            # print(dumps(cursor, indent=2))
            result.append(dumps(cursor))

    if protocol!="":
        cursor = current_db.find({"protocols":{ "$regex": re.compile(protocol, re.IGNORECASE)}},{"protocols":1,"id":1,"_id":0,"name":1})
        result.append(dumps(cursor))

    if tag != "":
        cursor = current_db.find({"tags":{ "$regex": re.compile(tag, re.IGNORECASE)}}, {"tags": 1, "id": 1, "_id": 0,"name":1})
        result.append(dumps(cursor))

    if category != "":
        cursor = current_db.find({"category":{ "$regex": re.compile(category, re.IGNORECASE)}}, {"category": 1, "id": 1, "_id": 0,"name":1})
        # print(dumps(cursor, indent=2))
        result.append(dumps(cursor))

    if summary!="":
        cursor = current_db.find({"summary":{ "$regex": re.compile(summary, re.IGNORECASE)}},{"summary":1,"id":1,"_id":0,"name":1})
        result.append(dumps(cursor))

    if description!="":
        cursor = current_db.find({"description":{ "$regex": re.compile(description, re.IGNORECASE)}},{"description":1,"id":1,"_id":0,"name":1})
        result.append(dumps(cursor))
    if label != "":
        cursor = current_db.find({"label": {"$regex": re.compile(label, re.IGNORECASE)}},
                                 {"label": 1, "id": 1, "_id": 0, "name": 1})
        result.append(dumps(cursor))

    if APIname!="":
        limiter=random.randint(1,100)
        skipper=abs(limiter-random.randint(1,100))
        cursor = current_db.find({"API":{"$exists":"true"}},{"description":1,"id":1,"_id":0,"name":1,"API":1}).limit(limiter).skip(skipper)
        # print(type(cursor))
        result.append(dumps(cursor))


    # print(result)
    return result
