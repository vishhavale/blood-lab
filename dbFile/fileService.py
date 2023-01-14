import os
from werkzeug.utils import secure_filename
from flask import request
from random import *
import string
import calendar
import time


UPLOAD_FOLDER = 'static/services/form_data'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getTimeDate():
    current_GMT = time.gmtime()
    return calendar.timegm(current_GMT)

#first store in db
def uploadFile(files=None,filePath=UPLOAD_FOLDER):
    files = request.files['file']
    filename = files.filename
    if files != None:
        try:
            if filePath != UPLOAD_FOLDER: filePath = UPLOAD_FOLDER + filePath
            if files and allowed_file(filename):
                filename =secure_filename(str(getTimeDate())+"_"+filename)
                files.save(os.path.join(filePath, filename))
                return True,UPLOAD_FOLDER+"/"+filename
        except Exception as e:
            print("upload file exception",e)
    return False,""

def deleteFile(filepath):
    try:
        if os.path.exists(filepath):
            print("yes")
            os.remove(filepath)
            print("yes2")
            return True
        else:
            print(filepath,"not available")
    except Exception as e:
        print("exception while delete file from local",e)
    return False