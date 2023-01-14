from flask import Blueprint,redirect,url_for
import sys
sys.path.append('..')
from handler.renderHandler import *

userBluePrint = Blueprint('', __name__,template_folder='templates')
@userBluePrint.route('',methods=['GET'])
def index():
    return redirect(url_for('Dashboard'))

@userBluePrint.route('dashboard',methods=['GET'])
def Dashboard():
    return render('dashboard')
    
@userBluePrint.route("getServices",methods=['GET'])
def Services():
    print("dsd")
    return render("GET_SERVICES")
    #return render('ShowAllService')

@userBluePrint.route("dashboard/services/onboard",methods=['GET','POST'])
def ServiceOnboard():
    return render("ServicesOnboard")

@userBluePrint.route("dashboard/services/statuses",methods=['GET'])
def ServicesStatus():
    return render("ServicesStatus")
    
@userBluePrint.route("dashboard/services/statuses/Details",methods=['GET'])
def ServicesStatusDetails():
    return render("ServicesStatusDetails")

@userBluePrint.route("dashboard/services/details/tracker",methods=['GET'])
def ServicesDetailsTracker():
    return render("ServicesDetailsTracker")

@userBluePrint.route("getTransactions",methods=['GET','POST'])
def Transactions():
    return render("TRANSACTION")

@userBluePrint.route("dashboard/transactions/Details",methods=['GET'])
def TransactionsDetails():
    return render("TransactionsDetails")

@userBluePrint.route("/dashboard/services/serviceAdministrator",methods=['GET'])
def serviceAdministrator():
    return render("serviceAdministrator")


@userBluePrint.route("getWalleteDetails",methods=['GET'])
def walleteDetails():
    return render("WALLETE_DETAILS")

@userBluePrint.route('/user',methods=['GET','POST'])
def user():
    return render('user')

@userBluePrint.route('/uploadFormFiles',methods=['POST'])
def uploadFormFiles():
    return render("UPLOAD_FORM_FILES")

@userBluePrint.route('/setFormData',methods=['POST'])
def saveFormData():
    return render("SAVE_FORM_DATA")

@userBluePrint.route('removeFile',methods=['POST'])
def removeFile():
    return render("DELETE_FILE")

@userBluePrint.route('/getFormData',methods=['GET'])
def getFormData():
    return render("GET_FORM_DATA")