
import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['test']
collection = db['students']

# 在 MongoDB 中，每条数据其实都有一个_id属性来唯一标识。如果没有显式指明该属性， MongoDB 会自动产生一个 Objectid 类型的_id 属性 。 insert()方法会在执行后返回_id 值
student1 = {
    'id': '20120001',
    'name':'Jim',
    'age':23.5,
    'gender':'male'
}
student2 = {
    'id': '20120001',
    'name':'Jack',
    'age':25,
    'gender':'male'
}
id(student1)
id(student2)
# result = collection.insert([student1, student2]) # 不考虑是否是重复数据,但考虑是否内存id是否是一样
# print(result)
#  官方推荐使用 insert_one()和 insert_many()方法来分别插入单条记录和多条记录
# result = collection.insert_one(student1)
# result.inserted_id
result = collection.insert_many([student1, student2])
result.inserted_ids


# 查询
# result = collection.find_one({'name':'Jim'})
# result
# result = collection.find({'name':'Jim'})
# for item in result:
#     print(item)

# from bson.objectid import ObjectId
# result = collection.find_one({'_id':ObjectId('5ccd7145cb03ace944fb907e')})
# result

result = collection.find({'age':{'$gt':24}})
for item in result:
    print(item)
    
result = collection.find({'name':{'$regex': '^Ja.*'}})
for item in result:
    item

result = collection.find({'$where':'obj.name == "Jack"'})
result.count()
for item in result:
    item
    
# 更新
condition = {'name': 'Jack'}
student = collection.find_one(condition)
student['age'] = 21
result = collection.update(condition, student)
result
result = collection.update_one(condition, {'$set':student})
result.matched_count, result.modified_count

# 满足条件的年龄都加1
condition = {"age": {"$gt":20}}
result = collection.update_many(condition, {"$inc":{"age":1}})
result.matched_count, result.modified_count

# 删除
collection.remove({'name':'Jim'})
collection.delete_one({'name':'Jim'})
collection.delete_many({'name':'Jim'})
