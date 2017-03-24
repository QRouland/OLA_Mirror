from app.api.GroupAPI import GroupAPI
from app.api.LoginAPI import LoginAPI
from app.api.UserAPI import UserAPI
from app.api.UserInfoAPI import UserInfoAPI
from app.api.exampleapi import SomeApi
from app.core import api

# Some Api resource
api.add_resource(SomeApi, '/api/someapi', '/api/someapi/<int:id>')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(UserInfoAPI, '/api/userInfo')
api.add_resource(UserAPI, '/api/user', '/api/user/byuid/<int:uid>', '/api/user/byemail/<string:email>')
api.add_resource(GroupAPI, '/api/group', '/api/group/bygid/<int:gid>', '/api/group/byname/<string:name>')
