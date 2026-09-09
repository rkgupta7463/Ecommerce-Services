from ninja import NinjaAPI,Router,Schema
from ...utility import *
from ...queries.user_query import *

app=Router()

@app.get("health-check/")
def health_check(request):
    return {"status":True,"message":"working fine!","status_code":200}

class UserCreationSchema(Schema):
    first_name:str
    last_name:str
    email:str
    plain_pass:str
    phone:str


@app.post("signup/")
def signup_user(request,payload:UserCreationSchema):
    try: 
        data=payload.dict()
        #check if email already exist
        exist_email=get_emailid(email=payload.email)
        if exist_email:
            return {"status":False,"message":"Email id is already exist!"}

        data['plain_pass']=HashHelper.get_password_hash(plain_password=data['plain_pass'])

        result=user_create(data=data)
            
        return {"status":True,"message":"signed up successfully!","data":result}
    except Exception as e:
        return {"status":False,"message":f"Expection {e}"}

class UserLoginSchame(Schema):
    email:str
    password:str

@app.post("login/")
def login_user(request,payload:UserLoginSchame):
    try:
        # check the email exist or not
        exist=get_emailid(email=payload.email)
        if exist:
            user_info=get_user_info_by_email(email=payload.email)
            print("user info:- ",user_info)
            if user_info:
                if HashHelper.verify_password(plain_password=payload.password,hashed_password=user_info[3]):
                    token=AuthHandler.sign_jwt(user_id=user_info[0])
                    if token:
                        return {"status":True,"access_token":token}
                    raise {"status":False,"message":"Unable to process the request."}
                else:
                    raise {"status":False,"message":"Please check your Credentials!"}     
    except Exception as e:
        return {"status":False,"message":f"Expection {e}"}


@app.post("get-user-info/")
def get_user_details(request,user_id):
    try:
        user_detail=get_user_info_by_id(user_id=user_id)
        if user_detail:
            return {"status":True,"message":"user info!","data":{"id":user_detail[0],"name":user_detail[1],"email":user_detail[2],"phone":user_detail[3]}}
        else:
            return {"status":False,"message":f"User not found"}
            
    except Exception as e:
        return {"status":False,"message":f"Expection {e}"}

