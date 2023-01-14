from flask import request
from generic.genericDb import *
from generic.requestAndResponse import *
from auth import *
def restHandler(mysql,table):
    
    if request.method=="GET" :
        dicts = TransFormRequest()
        id = dicts.get('id')
        if id is None:
            data = get(mysql,table,["*"])
        else:
            data = get(mysql,table,["*"],"WHERE id='"+str(id)+"'")
        return response(200,data,"")
    elif request.method=="POST":
        dicts = TransFormRequest()
        if(create(mysql,table,dicts)):
            return response(200,"created Successfully","")
        return response(400,"failed","error during creation")
    if request.method=="PUT":
        dicts = TransFormRequest()    
        id = str(dicts.get('id'))
        if(id==str(None)):
            return response(401,"","Please Provide Required Fields")            
        if(put(mysql,table,dicts,condition="WHERE id="+id)):
            return response(200,"updated successfully","")
        else:
            return response(401,"","failed")
    if request.method=="DELETE":
        dicts = TransFormRequest()
        id = dicts.get('id')
        if(id==str(None)):
            return response(401,"","Please Provide Required Fields")
        elif(delete(mysql,table,[],condition="WHERE id"+id)):
            return response(200,"deleted successfully","")
        else:
            return response(401,"","failed")