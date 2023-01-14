import sys,os
from dotenv import load_dotenv
sys.path.append('..')
from generic import *
from dbFile import *
import mysql
from auth import *
load_dotenv()

cntx = None
def createConnection():
    return mysql.connector.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    database=os.environ['DB_NAME']
    )

def render(template):
    res,user = Verified()
    if res == False:
        return response(401,"","unauthorized user")    
    cntx = createConnection()
    if template == "getServicesFile":
        if request.method == "POST":
            data = [{"type":"Banking","icon":"bank.png"},{"type":"Bill Payment","icon":"bill.png"},{"type":"Travels","icon":"travel.png"},{"type":"Loan","icon":"loan.png"},{"type":"Insurance","icon":"health-insurance.png"},{"type":"eGovernance","icon":"government.png"},{"type":"GST & Income Tax","icon":"tax.png"},{"type":"Business","icon":"business.png"},{"type":"Licenses & Registrations","icon":"lisence.png"},{"type":"Affidavit & Agreement","icon":"legal-document.png"},{"type":"Trademark","icon":"trademark.png"}]
            return response(200,data,"")
            
    if template =="UPLOAD":
        #make response
        status,fileName = uploadFile()
        #get upload file insert 
        data = {
            "name":fileName,
            "user_id":user.get('id')
        }
        if status:
            status,id = create(cntx,"file_data",data)
            print("status upload",status,id)
            if status:
                cntx.commit()
                return response(200,data={
                    "id":id
                },error="")

        return response(501,"file not uploaded","")
    return response(501,"","Url Not Available")