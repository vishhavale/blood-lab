import os
from generic import *
from flask import request
from auth import *
import mysql
from rediss import *


cntx = None
def createConnection():
    return mysql.connector.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    database=os.environ['DB_NAME']
    )

def render(template):
    cntx = createConnection()
    if template=="LOGIN":
        data = TransFormRequest()
        if data.get("password")!=None and data.get("id")!=None:
            query = "select * from user where mobile='{mobile}' and password='{password}'".format(mobile=data.get("id"),password=data.get("password"))
            tempData = rawQuery(cntx,query,type="SELECT",fetch="one")
            if len(tempData)>0:
                print("sandesh")
                enc_data = {
                    "id":tempData["id"],
                    "fname":tempData["fname"],
                    "lname":tempData["lname"],
                    "mobile":tempData["mobile"]
                } 
                tempEnc = createToken(enc_data)
                createKeyObject("{id}-{mobile}".format(id=tempData['id'],mobile=tempData['mobile']),tempEnc)
                return response(200,data={"status":"success",'authToken':tempEnc},error="")
        return response(200,"",error="please provide valid credientials")
    return response(501,"",error="Invalid Api")
