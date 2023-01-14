from flask import Blueprint,redirect,url_for
import sys
sys.path.append('..')

from handler.FileHandler import *
filemanager = Blueprint('file',__name__,template_folder='templates',url_prefix="/file")

@filemanager.route('/getServicesFile',methods=['POST'])
def getServicesFile():
    return render('getServicesFile')

@filemanager.route('/fileUpload',methods=['POST'])
def uploadFile():
    return render("UPLOAD")
