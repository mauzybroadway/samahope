from pymongo import MongoClient
client = MongoClient()

db = client.test_database
collection = db.test_collection

post = {"name":"sexybeast",
	"quest":"grails",
	"de la":["soul","ghetto"]}

posts = db.posts
posts.insert(post)

print db.collection_names(include_system_collections=False)

for post in posts.find():
  print post
