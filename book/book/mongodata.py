from pymongo import MongoClient
import os
import json


def saveMongodb(document_loc):
    # Password for mongodb saved in ~/.bashrc file
    client = MongoClient('mongodb+srv://krishjoshi02:' + os.environ.get("mongoidpass") + '@atlasclusterkrish.bfq65vf.mongodb.net/')
    
    db = client.scrapybooks
    collection = db.book_collection

    with open(document_loc,"r") as file:
        jsonfile = json.load(file)

    count=0
    for record in jsonfile:
        # Print details
        '''print("url : " + record["url"])
        print("book_name : " + record["book_name"])
        print("book_price : " + record["book_price"])
        print("category : " + record["category"])
        print("rating : " + record["rating"])'''

        id = collection.insert_one(record).inserted_id
        print("ID for record : " + str(id))
        count+=1

    print("Number of json records inserted : " + str(count))

saveMongodb(document_loc = "/Users/krishjoshi/Desktop/Python/WebScraping/Output/bookdata.json")