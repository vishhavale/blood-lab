import jwt
from flask import request
from rediss import *
def createToken(payload): 
    encoded = jwt.encode(payload,"sandeshrathod09702086914848", algorithm="HS256")
    return encoded

def decodeToken(payload):
    decode = jwt.decode(payload,"sandeshrathod09702086914848", algorithms=["HS256"])
    return decode

def Verified():
    if 'Access-token' in request.headers:
        accessToken = request.headers['Access-token']
        if accessToken !=None:
            try:
                data = decodeToken(accessToken)
                usertoken = getKeyObject("{id}-{mobile}".format(id=data.get("id"),mobile=data.get("mobile")))
                if len(usertoken)>0:
                    return True,data
                else:
                    return False,{}
            except Exception as err:
                print("execption while decode auth token",err)
            return False,{}
    else:
        return False,{}