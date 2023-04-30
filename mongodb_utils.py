import json
import pandas as pd
from pymongo import MongoClient 

def load_db():

	myclient = MongoClient("mongodb://localhost:27017/")

	db = myclient["academicworld"]

	with open('faculty.json') as file:
		file_data = json.load(file)

	Collection = db["faculty"]

	if isinstance(file_data, list):
		Collection.insert_many(file_data)
	else:
		Collection.insert_one(file_data)
		

	with open('publications.json') as file:
		file_data = json.load(file)

	Collection = db["publications"]

	if isinstance(file_data, list):
		Collection.insert_many(file_data)
	else:
		Collection.insert_one(file_data)

def get_keywords_monogo():
	client = MongoClient("localhost", 27017, maxPoolSize=50)
	db = client.academicworld

	#query = ([{"$unwind":"$keywords"},{"$match":{"keyword.name":"machine learning"}},
		  #{"$group":{"_id":"$keywords.name", "year":1}},{"$sort":{"pub_cnt":-1}},{"$limit":10}])
	query = ([{'$unwind':'$keywords'},{'$group':{'_id':'$keywords.name'}}])
	keywords =[]
	for x in db.publications.aggregate(query):
		keywords.append(x['_id'])
	return keywords

def keyword_per_year_mongo(keyword):
	client = MongoClient("localhost", 27017, maxPoolSize=50)
	db = client.academicworld
	query = ([{'$unwind':'$keywords'},{'$match':{"keywords.name":str(keyword)}},
	    {'$group':{'_id':'$year', "count":{'$sum':1}}},{'$sort':{'_id':1}},{'$limit':10}])
	dict = {'year':[], 'count':[]}
	for x in db.publications.aggregate(query):
		dict['year'].append(x['_id'])
		dict['count'].append(x['count'])
	return dict	




