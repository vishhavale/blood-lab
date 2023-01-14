from flask import request,json,jsonify,make_response

def TransFormRequest():
    try:
        if request.method in ["POST","PUT"]:
            res = request.get_data("data")
            jsons = json.loads(res)  
            return jsons        
        if request.method in ["GET","DELETE"]:
            args = request.args
            data = args.to_dict()
            return data
    except Exception as e:
        print("Exception during transform request",e)
    return {}

def response(status=200,data="",error=""):
    return make_response(
                jsonify(
                    {"data":data,"error": error}
                ),
                status,
            )