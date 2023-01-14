from flask import jsonify,render_template,request,make_response
import sys
from generic.genericDb import create, rawQuery
from generic.requestAndResponse import response
sys.path.append('..')
from generic import TransFormRequest
import base64
from generic import get
from dbAdmin import services 
from rediss import *
from .tempData import formData

datas = formData.data
def filterAffidavit(item):
    for i in datas:
        if item == i.get('base64'):
            return True,i.get('name')
    return False,""

def Services(mysql):
    data = getKeyObject('servicesDetails')
    if len(data)>0:
        mysql.close()
        return response(200,data=data,error="")
    query = "select ser.id,ser.name,ser.amount,stype.name as type from services ser inner join servicetypes stype on stype.id=ser.servicetype_id"
    data = rawQuery(mysql,query,type="SELECT",fetch="all")
    arr_type = {}
    array = []
    for i in data:
        temp = i.get('type')
        if temp not in array:
            array.append(temp)
            arr_type[temp] = list(filter(lambda x: x.get('type')== temp, data))
    mysql.close()
    if createKeyObject('servicesDetails',arr_type):
        return response(200,data,error="")
        
def ServicesOnboard(mysql):
    dicts = TransFormRequest()
    if dicts.get("key") != None:
        status,form_name =filterAffidavit(dicts.get("key"))
        if status:
            data = get(mysql,"services",["*"],"where service_name='"+str(form_name)+"'","one")
            context = {"data":data}
            return render_template("user/services/masterForm.html",context=context)
        else:
            return response(404,"","page Not Found")

def ServicesStatus(mysql):
    query = "SELECT fd.id,fd.full_name,fd.created_at,sc.service_name FROM form_data fd left join services sc on sc.id=fd.service_id where fd.is_deleted=0"
    data = rawQuery(mysql,query,type="SELECT",fetch="all")
    context = {"data":data}
    return render_template("user/ApplicationStatus/servicesStatus.html",context=context)
    
def ServicesStatusDetails(mysql):
    data = TransFormRequest()
    if data.get('key')== None:
        return response(404,"","page not found")
    query = "select fd.*,tr.* from form_data fd left join Transactions tr on tr.transaction_number=fd.transactionNo where fd.id="+str(data.get('key'))+" and fd.is_deleted=0"
    data = rawQuery(mysql,query,type="SELECT",fetch="one")
    return response(200,data,"")
    
def serviceInfo(mysql,Name):
    query = "select * from services where name='{name}'".format(name=Name)
    data = rawQuery(mysql,query,type="SELECT",fetch="one")
    return data

def ServicesDetailsTracker(mysql):
    data = TransFormRequest()
    if data.get('form_id')!=None:
        query = "SELECT `id`,`status`,`document` FROM `services_administrator` WHERE Form_id='"+data.get('form_id')+"'"
        data = rawQuery(mysql,query,type="SELECT",fetch="one")
        return response(200,data,"")
    return response(404,"","page not found")

def serviceAdministrator(mysql):
    data = TransFormRequest()
    if data.get('form_id')!= None:
        query = "select file_type,file,status,from_status,create_at from services_administrator where form_id={form_id} and is_deleted=0".format(form_id=data.get('form_id'))
        data = rawQuery(mysql,query,type="SELECT",fetch="all")
        return response(200,data,"")
    return response(401,"","please provide parameters")

def walleteDetails(mysql):
    data = TransFormRequest()
    if data.get('id') != None:
        query = "select amount from wallete where user_id={id}".format(id=data.get('id'))
        data = rawQuery(mysql,query,type="SELECT",fetch="one")
        return response(200,data,"")
    return  response(401,"","please provide parameters")
