from flask import Blueprint,redirect,url_for
import sys
from handler.patient_handler import*
sys.path.append("..")
userBluePrint = Blueprint('',__name__,template_folder='templates')
@userBluePrint.route('/RegisterPatient', methods=['POST'])
def registerPatient():
    return render('registerp')

@userBluePrint.route('/GetPatients', methods=['GET'])
def getPatient():
    return render('getPatient')

@userBluePrint.route('/UpdatePatient',methods=['POST'])
def updatePatients():
    return render('updatePatient')
