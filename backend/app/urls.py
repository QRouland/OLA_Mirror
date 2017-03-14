from app.api.UserAPI import UserAPI
from app.api.UserInfoAPI import UserInfoAPI
from app.api.exampleapi import SomeApi
from app.api.loginAPI import LoginAPI
from app.core import api

# Some Api resource
api.add_resource(SomeApi, '/api/someapi', '/api/someapi/<int:id>')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(UserAPI, '/api/user', '/api/user/byuid/<int:uid>', '/api/user/bylogin/<string:login>',
                 '/api/user/byemail/<string:email>')
api.add_resource(UserInfoAPI, '/api/userInfo')
