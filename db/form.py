import sys,os
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from flask import request,make_response,jsonify
from generic import *
from wallet import *
from .services import *
from Transactions import *
from threading import active_count
sys.path.append('..')
from dbFile.fileService import uploadFile

def InsertAffidavitAndLegal(mysql):
    try:
        data = TransFormRequest()
        ids = data.get('service_id')
        user_id = data.get('user_id')
        form_info = get(mysql,"services",['service_name','price','commission','comm_type'],"where id='"+str(ids)+"'","one")
        price = form_info.get('price')
        commission = form_info.get('commission')
        comm_type = form_info.get('comm_type')
        wl = Wallet(mysql,user_id)
        status,code = wl.ServiceWallete(commission,price,comm_type) 
        if status:
            data_wallet = {
                "closing_balance":wl.closing_balance,
                "opening_balance":wl.opening_balance,
                "commission":wl.commission,
                "transaction_amount":str(wl.transaction_amount),
                "wallet_id":wl.wallet_info.get("id"),
                "user_id":user_id,
                "transaction_for":form_info.get("service_name"),
                "transaction_type":"debit"
            }
            transactions = Transactions(mysql)
            st,transNo = transactions.registerTransaction(data_wallet)
            if st:
                data["transactionNo"] = transNo
                status,id = create(mysql,"form_data",data)
                if status:
                    return jsonify(status="success",data={"id":id},error="")
            else:
                return response(501,"","transaction Failed your amount will be credited after 1 working days")
        mysql.rollback()
        status = ""
        for i in wl.status_return_code:
            if(i.get('code')==code):
                status = i.get('status')            
        return jsonify(status="failed",data="",error=status)
    except Exception as e:
        mysql.rollback()
        return response(500,"",e)

def uploadFormFiles(cntx,user_id):
    res,file = uploadFile()
    if res != None:
        data_dict = {
            "name":file,
            "user_id":user_id
        }
        res,data = create(cntx,"file_data",data_dict)
        if res:
            cntx.commit()
            return response(200,data={"id":data},error="")
    return response(500,data="",error="fail to upload")

def insertFormData(cntx,data,user):
    query = "insert into form_data(`first_name`,`last_name`,`user_id`,`mobile`,`email`) values('{firstName}','{lastName}',{id},'{mobile}','{email}')".format(firstName=data['firstName'],lastName=data['lastName'],id=user.get('id'),mobile=data['mobileNumber'],email=data['email'])
    return rawQuery(cntx,query,type="INSERT")

def insertFormGeos(cntx,data):
    query = "insert into form_geos(`state_name`,`district`,`city`,`pincode`) values('{stateName}','{district}','{city}','{pincode}')".format(stateName=data['state'],district=data['district'],city=data['city'],pincode=data['pincode'])
    return rawQuery(cntx,query,type="INSERT")

def insertServiceForm(cntx,form_id,service_id):
    query = "insert into form_services(form_id,service_id) values({form_id},{service_id})".format(form_id=form_id,service_id=service_id)
    return rawQuery(cntx,query,type="INSERT")
    
def insertFileData(cntx,data,form_id):
    if len(data["fileId"])>0:
        query = "insert into file_with_form_data(`form_id`,`file_id`) values"
        for i in data["fileId"]:
            query = query + "({formId},{id}),".format(formId=form_id,id=i)
        query = query[0:len(query)-1]
        print(query)
        return rawQuery(cntx,query,type="INSERT")
    return 0

def insertAddressData(cntx,data,form_id,geos_id):
    query = "insert into form_address(`form_address`,`form_id`,`form_geo_id`) values('{address}',{formId},{formGeoId})".format(address=data["address"],formId=form_id,formGeoId=geos_id)
    return rawQuery(cntx,query,type="INSERT")

def CalculationsAndTransactions(cntx,form_service,serviceDetails,user_id):
    try:
        wal = Wallet(cntx,user_id)
        if wal.getWallet():
            if form_service>0:
                commissionType = 1 if serviceDetails.get('commission_type')=="float" else 2 
                wal.ServiceWallete(serviceDetails.get('commission'),serviceDetails.get('amount'),commissionType)
                print(wal.Status)
                if wal.Status==200:
                    data_wallet = {
                                "closing_balance":wal.closing_balance,
                                "opening_balance":wal.opening_balance,
                                "commission":wal.commission,
                                "transaction_amount":str(wal.transaction_amount),
                                "wallet_id":wal.wallet_info.get("id"),
                                "user_id":user_id,
                                "transaction_for":serviceDetails.get("name"),
                                "transaction_type":"debit"
                    }
                    transactions = Transactions(cntx)
                    status,transNo = transactions.registerTransaction(data_wallet)
                    if status:
                        return True
    except Exception as e:
        print("exception while create transactions",e)
    return False

def saveFormData(cntx,user):
    try:
        wal = Wallet(cntx,user.get('id'))
        cntx.autocommit = False
        if wal.getWallet():
            data = TransFormRequest()
            print(data)
            with ThreadPoolExecutor(max_workers=1) as exe:
                form_db= exe.submit(insertFormData,cntx,data,user)
                form_geos = exe.submit(insertFormGeos,cntx,data)
                service = exe.submit(serviceInfo,cntx,data['service'])      
            form_id,geos_id = form_db.result(),form_geos.result()
            serviceDetails = service.result()
            with ThreadPoolExecutor(max_workers=1) as exe:
                file_data = exe.submit(insertFileData,cntx,data,form_id)
                geos_data = exe.submit(insertAddressData,cntx,data,form_id,geos_id)
                form_service = exe.submit(insertServiceForm,cntx,form_id,serviceDetails.get('id'))
            geos_data.result()
            file_data.result()
            formService = form_service.result()
            if CalculationsAndTransactions(cntx,formService,serviceDetails,user.get('id')):
                cntx.commit()
                cntx.close()
                return response(200,data="successfully submited",error="")
    except Exception as e:
        print("exception while save form ",e)
    cntx.rollback()
    cntx.close()
    return response(500,data="",error="Error while inserting data")
def getFormData(cntx,user_id):
    try:
        query = "select form.id,form.first_name,form.last_name,form.middle_name,form.created_at as app_date,form.status,form.mobile,form.email,form_geos.state_name,"
        query += "form_geos.district,form_geos.city,form_geos.pincode,addr.form_address,"
        query += "services.name as service_name from form_data form inner join form_address " 
        query += "addr on addr.form_id=form.id inner join form_geos on form_geos.id=addr.form_geo_id "
        # query += "inner join file_with_form_data files on files.form_id=form.id "
        # query += "inner join file_data on file_data.id=files.file_id "
        query += "inner join form_services fservice on fservice.form_id=form.id "
        query += "inner join services on services.id=fservice.service_id where form.user_id={id}"
        print(query)
        query = query.format(id=user_id)
        data = rawQuery(cntx,query,type="SELECT")
        if data == None or len(data)==0:
            data = []
        return response(200,data=data,error="")
    except Exception as e:
        print("heool",e)
    return response(501,"","internal error")