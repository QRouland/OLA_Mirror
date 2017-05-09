from app.api.GetAllAPI import GetAllAPI
from app.api.GroupAPI import GroupAPI
from app.api.LivretAPI import LivretAPI
from app.api.LoginAPI import LoginAPI
from app.api.PeriodAPI import PeriodAPI
from app.api.UserAPI import UserAPI
from app.api.UserInfoAPI import UserInfoAPI, UserGroupsAPI
from app.api.exampleapi import SomeApi
from app.core import api

# Some Api resource
api.add_resource(SomeApi, '/api/someapi', '/api/someapi/<int:id>')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(UserInfoAPI, '/api/userInfo')
api.add_resource(UserGroupsAPI, '/api/userGroups')
api.add_resource(UserAPI, '/api/user', '/api/user/byuid/<int:uid>', '/api/user/byemail/<string:email>',
                 '/api/user/byhash/<string:hashcode>')
api.add_resource(GroupAPI, '/api/group', '/api/group/bygid/<int:gid>', '/api/group/byname/<string:name>')
api.add_resource(LivretAPI, '/api/livret', '/api/livret/bylid/<int:lid>',
                 '/api/livret/bytutorship/<int:group_id>/<int:student_id>')
api.add_resource(PeriodAPI, '/api/period', '/api/period/bypid/<int:pid>')
api.add_resource(GetAllAPI, '/api/getAll/<string:what>/<int:value>')
