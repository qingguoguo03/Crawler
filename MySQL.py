
MySQL：cursor()方法获得MySQL的操作游标，利用游标来执行 SQL 语句
import pymysql
db = pymysql.connect(host='localhost',user='root' , password='', port=3306)
cursor = db.cursor()
# cursor.execute('select version()')
# cursor.fetchone()
# cursor.execute('show databases;')
# cursor.fetchone()
# cursor.execute('create database spiders default CHARACTER SET utf8;')
cursor.execute('show databases;')
cursor.fetchall()
db.close()


db = pymysql.connect(host='localhost',user='root' , password='', port=3306, db='spiders')
cursor = db.cursor()
sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY (id ))' 
cursor.execute(sql) 
db.close()

#  查询数据fetchone()方法来获取所有数据，而不是用 fetchall()全部结果以元组问部返回如果数据量很大那占用开销会非常高。 因此，推荐使用fetchone的方法
def insert_data(cursor, table, data):
    
    if not isinstance(data, list): # 所有单条记录全部转为list 都以插入多条记录的形式执行
        data = [data]   
    try:
        keys = ','.join(data[0].keys())
        values = ','.join(['%s']*len(data[0]))
        sql = 'insert into {table}({keys}) values ({values}) on duplicate key update '.format(table=table, keys=keys, values=values)
        update = ','.join(["{key}=values({key})".format(key=key) for key in data[0]])
        sql += update
        if cursor.executemany(sql, [tuple(item.values()) for item in data]):     
            print('Data updated successfully！')
            db.commit()
        else:
            print('Data already exists!')
    except Exception as e:
        print(e)
        db.rollback()
    

def select_data(cursor, table, condition='1', keys='*', limit=None):
    
    sql = 'select {keys} from {table} where {condition} {limit}'.format(keys=keys, table=table, condition=condition, limit='' if not limit else 'limit %d'%limit)
    try:
        cursor.execute(sql)
        print('count: ', cursor.rowcount)
        row = cursor.fetchone()
        while row:
            yield row
            row = cursor.fetchone()
    except Exception as e:
        print(e)
            
def delete_data(cursor, table, condition='1'):
    
    sql = 'delete from {table} where {condition}'.format(table=table, condition=condition)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)

db = pymysql.connect(host='localhost',user='root' , password='', port=3306, db='spiders')
cursor = db.cursor()
table = 'students'
# data = {
#     'id': '20120001',
#     'name':'Jim',
#     'age':25
# }
# insert_data(cursor, table, data)
# for row in select_data(cursor, table):
#     print(row)
# data = [
#     {
#         'id': '20120001',
#         'name':'Jim',
#         'age':23.5
#     },
#     {
#         'id': '20120002',
#         'name':'Jane',
#         'age':24
#     },
#     {
#         'id': '20120004',
#         'name':'Jack',
#         'age':26
#     }
# ]
# insert_data(cursor, table, data)
delete_data(cursor, table, 'age>24')
for row in select_data(cursor, table):
    print(row)
    
    
 
