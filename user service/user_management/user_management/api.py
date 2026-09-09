from main_app.apis.v1.users import app as user_api
from ninja import NinjaAPI,Redoc


app=NinjaAPI(title="Ecommerce APIs")#,docs=Redoc()

app.add_router('v1',user_api)