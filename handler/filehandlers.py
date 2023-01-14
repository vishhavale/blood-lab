import os
from werkzeug.utils import secure_filename
from flask import request
from random import *
import string

UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(files,filePath=UPLOAD_FOLDER):
    try:
        if filePath != UPLOAD_FOLDER: filePath = UPLOAD_FOLDER + filePath
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(''.join(random.choices(string.ascii_lowercase, k=9))+'andesh')
                file.save(os.path.join('', filename))
                return True
    except Exception as e:
        print("upload file exception",e)
    return False

def once_upload_file(file,filePath):
    try:
        if filePath != UPLOAD_FOLDER: filePath = UPLOAD_FOLDER + filePath
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("FDF",filename)
            print("d",filePath)
            file.save(os.path.join('', filePath+filename))
            return True
    except Exception as e:
        print("upload file exception",e)
    return False