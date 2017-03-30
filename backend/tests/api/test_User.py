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
        query = USER.delete().where(user_class.email == "admin@admin.com")
        query.execute()
        query = USER.delete().where(user_class.email == "adminx@admin.com")
        query.execute()

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def create_user(self, email, role, name):
        return self.app.post('/api/user',
                             data=json.dumps(
                                 dict(
                                     email=email,
                                     role=role,
                                     name=name
                                 )
                             ), content_type='application/json')

    def getUserByID(self, UID):
        return self.app.get('/api/user/byuid/' + str(UID))

    def getUserByEmail(self, email):
        return self.app.get('/api/user/byemail/' + email)

    def change_user(self, UID, email, role, phone, name, password):
        return self.app.put('/api/user/byuid/' + str(UID),
                            data=json.dumps(
                                dict(
                                    role=role,
                                    email=email,
                                    phone=phone,
                                    name=name,
                                    password=password
                                )
                            ), content_type='application/json')

    def test_user(self):
        rv = self.create_user('admin@admin.com', '4', 'Admin')
        self.assertEqual(rv.status_code, 201, 'Creating user Failed')
        uid = json.loads(rv.data)['UID']
        self.assertIsNotNone(uid)

        rv = self.create_user('admin@admin.com', '4', 'Admin')
        self.assertEqual(rv.status_code, 200, 'User is supposed to already exist')
        uid2 = json.loads(rv.data)['UID']
        self.assertEqual(uid, uid2, "The UID must be the same !")

        rv = self.getUserByID(uid)
        self.assertEqual(rv.status_code, 200, 'Getting user failed by ID')
        user = json.loads(rv.data)['USER']
        self.assertIsNotNone(user)

        rv = self.getUserByEmail("admin@admin.com")
        self.assertEqual(rv.status_code, 200, 'Getting user failed by email')
        user3 = json.loads(rv.data)['USER']
        self.assertEqual(user, user3, "User by email must be the same !")

        rv = self.change_user(uid, 'adminx@admin.com', '3', '11.11.11.11.11', 'Adminx', 'password')
        self.assertEqual(rv.status_code, 200, 'User modification failed !')
        uid3 = json.loads(rv.data)['UID']
        self.assertEqual(uid, uid3, "UIDs doesn't match !")

        rv = self.getUserByEmail("adminx@admin.com")
        self.assertEqual(rv.status_code, 200, 'Getting modified user failed by Email')
        user4 = json.loads(rv.data)['USER']
        self.assertIsNotNone(user4, "Modified user shouldn't be None !")


if __name__ == '__main__':
    unittest.main()
