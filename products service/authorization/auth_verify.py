import jwt
from decouple import config
import time


JWT_SECRET=config('JWT_SECRET',default='iujhvearfabdfoiciuygiyuvghhjhv251465hjdfbcihig8465')
JWT_ALGORITHM=config('JWT_ALGORITHM',default='HS256')

class AuthHandler(object):

    @staticmethod
    def sign_jwt(user_id:int,role_id:str):
        payload={
            "user_id":user_id,
            "role_id":role_id,
            "expires":time.time()+300
        }

        token=jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)

        return token
    
    @staticmethod
    def decode_jwt(token:str)->dict:
        try:
            decode_token=jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
            # FIXED HERE
            return decode_token if decode_token["expires"] >= time.time() else None
        except Exception as e:
            print("unable to decode the token, error: ",e)
            return None
        
