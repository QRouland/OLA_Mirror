import unittest

from flask import json

from app.core import app
from app.model import USER, getUser


class AuthTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if getUser(login="admin") is None:
            query = USER.insert().values(login="admin", email="admin@admin.com", role="4", phone="00.00.00.00.00")
            query.execute()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def login(self, email, password):
        return self.app.post('/api/login',
                             data=json.dumps(
                                 dict(
                                     login=email,
                                     password=password
                                 )
                             ), content_type='application/json')

    def logout(self):
        return self.app.delete('/api/login')

    def test_login_logout(self):
        rv = self.login('admin', 'admin')
        self.assertEqual(rv.status_code, 200, 'Login as admin Failed')

        rv = self.logout()
        self.assertEqual(rv.status_code, 200, 'Logout Failed')

        rv = self.login('adminx', 'admin')
        self.assertEqual(rv.status_code, 401, 'Authentication from CAS has not failed for the invalid user xadmin !')

        rv = self.login('admin', 'adminx')
        self.assertEqual(rv.status_code, 401,
                         'Authentication from CAS has not failed for the invalid password xadmin !')

        rv = self.login('toto', 'toto')
        self.assertEqual(rv.status_code, 403, 'Authentication shouldn\'t be allowed for user toto !')


if __name__ == '__main__':
    unittest.main()
