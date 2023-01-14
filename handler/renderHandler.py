import sys,os
from db import *
from dbFile.fileService import deleteFile
from dotenv import load_dotenv
import mysql.connector
from auth import *
sys.path.append('..')
load_dotenv('')

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
    res,user = Verified()
    if res is False:
        return response(401,"","unothorized user")
    if template == "dashboard":
        return dashboard(cntx)
    if template=='user':
        if request.method=="POST":
            return addUser(cntx)
    if template=="GET_SERVICES":
        return Services(cntx)
    if template=="ServicesOnboard":
        if request.method=="GET":
            return ServicesOnboard(cntx)
        else:
            return InsertAffidavitAndLegal(cntx)
    if template=="ServicesStatus":
        return ServicesStatus(cntx)
    if template=="ServicesStatusDetails":
        return ServicesStatusDetails(cntx)
    if template=="TRANSACTION":
        if request.method=="GET":
            return getTransactions(cntx)
        if request.method=="POST":
            return targetedTransactions(cntx)
    if template=="TransactionsDetails":
        return TransactionsDetails(cntx)
    if template=="ServicesDetailsTracker":
        return ServicesDetailsTracker(cntx)
    if template=="serviceAdministrator":
        return serviceAdministrator(cntx)
    if template=="WALLETE_DETAILS":
        return walleteDetails(cntx)
    if template=="UPLOAD_FORM_FILES":
        return uploadFormFiles(cntx,user_id=user.get('id'))
    if template=="SAVE_FORM_DATA":
        return saveFormData(cntx,user)
    if template=="DELETE_FILE":
        data = TransFormRequest()
        if data.get("id") != None:
            query = "select * from file_data where id={id}".format(id=data.get("id"))
            print(query)
            d = rawQuery(cntx,query,type="SELECT",fetch="one")
            if len(d)>0:
                if deleteFile(d.get('name')):
                    err,res = delete(cntx,"file_data","where id={id}".format(id=d.get("id")))
                    if res:
                        return response(200,"success delete","")    
            cntx.commit()
            cntx.close()
    if template=="GET_FORM_DATA":
        return getFormData(cntx,user.get('id'))
    else:
        return response(501,"","Invalid API Service")



    # elif template == "formDetails":
    #     return actualForm(mysql)
    # #form handler
    # elif template=="frmoDetails":
    #     print('skdjk')
    #     return renderForm(mysql)

    # elif template in "formCnfDetails":
    #     return masterForm(mysql)
        
    # #user info
    # elif(template=="userGet"):
    #     dicts = TransFormRequest()
    #     id = dicts.get('id')
    #     if(id is None):
    #         data = get(mysql,'user',["*"])
    #     else:
    #         data = get(mysql,"user",["*"],"WHERE id='"+str(id)+"'")
    #     return response(200,data,"")
    # #wallet info
    # elif template=="wallet":
    #     if request.method=="GET":
    #         data = TransFormRequest()
    #         id = data.get('user_id')
    #         credit(id,mysql)
    #         return render_template("user/wallet.html")
            
    #     if request.method=="POST":
    #         # data = {
    #         #     "user_id":,
    #         #     "credit_amount":
    #         # }
    #         data = TransFormRequest()
    #         if(registerTransaction(data)):
    #             return response(200,"Created","")
    #         return response(401,"","Failed to Create Transaction")

    # elif template=="transactionReport":
    #     if(request.method=="POST"):        
    #         data = getTransaction(mysql,None,None)
    #         return response(200,data,"")
    #     else:
    #         return render_template("user/transaction-report.html")

    # elif template=="ApplicationReport":
    #     return render_template("user/Application-status.html")

    # elif(template=="userPost"):
    #     dicts = TransFormRequest()
    #     is_inserted,id = create(mysql,"user",dicts)    
    #     data = {"user_id":str(id)}
    #     print(data)
    #     if(create(mysql,"wallete",data)):
    #         return response(200,"User creted","")
    #     return response(401,"","user not created")
    
    # elif template=="getServicesDocuments":
    #     return getServicesDocuments(mysql)

    # elif template=="setServicesDocuments":
    #     return setServicesDocuments(mysql)

    # elif template=="getDocuments":
    #     return getDocuments()

    # else:
    #     return response(404,"","Page Not Found")
