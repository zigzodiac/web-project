import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["runoobdb"]
dblist = myclient.list_database_names()
if "runoobdb" in dblist:

    print "database exist"
print "11111"
print dblist
