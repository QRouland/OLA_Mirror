import unittest

from flask import json

from app.core import app
from app.model import USER, user_class


class UserTestCase(unittest.TestCase):
    uid = None
    gid = None
    tid = None

    @classmethod
    def tearDownClass(cls):
        query = USER.delete().where(user_class.login == "admin")
        query.execute()
        query = USER.delete().where(user_class.login == "adminx")
        query.execute()

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def create_user(self, login, role):
        return self.app.post('/api/user',
                             data=json.dumps(
                                 dict(
                                     CASid=login,
                                     role=role
                                 )
                             ), content_type='application/json')

    def getUserByID(self, UID):
        return self.app.get('/api/user/byuid/' + str(UID))

    def getUserByLogin(self, login):
        return self.app.get('/api/user/bylogin/' + login)

    def getUserByEmail(self, email):
        return self.app.get('/api/user/byemail/' + email)

    def change_user(self, UID, login, role, email, phone):
        return self.app.put('/api/user/byuid/' + str(UID),
                            data=json.dumps(
                                dict(
                                    CASid=login,
                                    role=role,
                                    email=email,
                                    phone=phone
                                )
                            ), content_type='application/json')

    def test_user(self):
        rv = self.create_user('admin', '4')
        self.assertEqual(rv.status_code, 201, 'Creating user Failed')
        uid = json.loads(rv.data)['UID']
        self.assertIsNotNone(uid)

        rv = self.create_user('admin', '4')
        self.assertEqual(rv.status_code, 200, 'User is supposed to already exist')
        uid2 = json.loads(rv.data)['UID']
        self.assertEqual(uid, uid2, "The UID must be the same !")

        rv = self.getUserByID(uid)
        self.assertEqual(rv.status_code, 200, 'Getting user failed by ID')
        user = json.loads(rv.data)['USER']
        self.assertIsNotNone(user)

        rv = self.getUserByLogin("admin")
        self.assertEqual(rv.status_code, 200, 'Getting user failed by Login')
        user2 = json.loads(rv.data)['USER']
        self.assertEqual(user, user2, "User by login must be the same !")

        rv = self.getUserByEmail("admin@ola.com")
        self.assertEqual(rv.status_code, 200, 'Getting user failed by email')
        user3 = json.loads(rv.data)['USER']
        self.assertEqual(user, user3, "User by email must be the same !")

        rv = self.change_user(uid, 'adminx', '3', 'adminx@email.com', '11.11.11.11.11')
        self.assertEqual(rv.status_code, 200, 'User modification failed !')
        uid3 = json.loads(rv.data)['UID']
        self.assertEqual(uid, uid3, "UIDs doesn't match !")

        rv = self.getUserByLogin("adminx")
        self.assertEqual(rv.status_code, 200, 'Getting modified user failed by Login')
        user4 = json.loads(rv.data)['USER']
        self.assertIsNotNone(user4, "Modified user shouldn't be None !")


if __name__ == '__main__':
    unittest.main()
