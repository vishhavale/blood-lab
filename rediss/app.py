import os
import redis
import json
def createConnection():
    return  redis.Redis(
        host=os.environ['REDIS_HOST'],
        port=os.environ['REDIS_PORT'], 
        password='')

def createKeyObject(key,value):
    r = createConnection()
    try:
        r.set(key,json.dumps(value))
        return True
    except Exception as e:
        print("Exception while set key value",e)
    return False

def getKeyObject(key):
    r = createConnection()
    try:
        data = r.get(key)
        if data==None:
            return json.loads('{}')
        return json.loads(data)
    except Exception as e:
        print("Exception while get key value redis",e)
    return json.loads('{}')
