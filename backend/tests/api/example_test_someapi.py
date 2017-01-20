from flask import json

from backend.app.core import app
import unittest


class AuthTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def login(self, email, password):
        return self.app.post('/api/auth',
                             data=json.dumps(
                                 dict(
                                     email=email,
                                     password=password
                                 )
                             ), content_type='application/json')

    def logout(self):
        return self.app.get('/api/auth')

    def create_user(self, email, password, confirm):
        return self.app.post('/api/user',
                             data=json.dumps(
                                 dict(
                                     email=email,
                                     password=password,
                                     confirm=confirm
                                 )
                             ), content_type='application/json')

    def get_user(self, user_id=None):
        if user_id:
            return self.app.get('api/user/{}'.format(user_id))
        return self.app.get('api/user')

    def delete_user(self, user_id):
        return self.app.delete('api/user/{}'.format(user_id))

    def get_status(self):
        return self.app.get('api/auth/status')

    def test_login_logout(self):
        rv = self.login('admin@admin.com', 'admin')
        self.assertEqual(rv.status_code, 204, 'Login as admin Failed')

        rv = self.get_status()
        self.assertEqual(rv.status_code, 200,
                         'Status problem : should be auth')

        rv = self.logout()
        self.assertEqual(rv.status_code, 204, 'Logout Failed')

        rv = self.login('adminx', 'admin')
        self.assertEqual(rv.status_code, 401)
        self.assertIn('Invalid email format', json.loads(rv.data)['message']['email'],
                      'Should return : invalid format email')

        rv = self.login('admin@admin.com', 'default')
        self.assertEqual(rv.status_code, 401)
        self.assertIn('invalid email/password', json.loads(rv.data)['message'],
                      'Login invalid password unexpected return')

        rv = self.login('admin@admin.comx', 'admin')
        self.assertEqual(rv.status_code, 401)
        self.assertIn('invalid email/password', json.loads(rv.data)['message'],
                      'Login with invalid mail unexpected retutn')

    def test_add_user(self):
        rv = self.create_user('paul@paul.fr', 'superpassword', 'superpassword')
        self.assertEqual(rv.status_code, 401,
                         'Not connected user shouldn\'t be allow to add user')

        rv = self.login('admin@admin.com', 'admin')
        self.assertEqual(rv.status_code, 204, 'Login as admin Failed')

        rv = self.create_user('paulatpaul.fr', 'superpassword', 'superpassword')
        self.assertEqual(rv.status_code, 401)
        self.assertIn('Invalid email format', json.loads(rv.data)['message']['email'],
                      'Should return : invalid format email')

        rv = self.create_user('paul@paul.fr', 'super', 'super')
        self.assertEqual(rv.status_code, 401)
        self.assertIn('Password minimum length 6', json.loads(rv.data)['message']['password'],
                      'Should return : Password minimum length 6')

        rv = self.create_user('paul@paul.fr', 'superpassword', 'superpass')
        self.assertEqual(rv.status_code, 401)
        self.assertIn('Password and confirmation are not the same', json.loads(rv.data)['message']['password'],
                      'Should return : Password and confirmation are not the same')

        rv = self.create_user('paul@paul.fr', 'superpassword', 'superpassword')
        self.assertEqual(rv.status_code, 201,
                         'Add user failed')

        rv = self.create_user('paul@paul.fr', 'superpassword', 'superpassword')
        self.assertEqual(rv.status_code, 401,
                         'Should not can add a user with a email already in user')
        self.assertIn('email already in use', json.loads(rv.data)['message'],
                      'Bad error message')

        rv = self.login('paul@paul.fr', 'superpassword')
        self.assertEqual(rv.status_code, 204,
                         'Can\' login with new user !')

        rv = self.get_status()
        self.assertEqual(rv.status_code, 200,
                         'Status problem : should be auth')
        new_user_id = json.loads(rv.data)['id']

        rv = self.get_user(new_user_id)
        self.assertEqual(rv.status_code, 200,
                         'Can\'t get the new user')
        self.assertEqual('paul@paul.fr', json.loads(rv.data)['email'],
                         'The new user email is invalid')

    def test_get_user(self):
        rv = self.get_user(user_id=1)
        self.assertEqual(rv.status_code, 401,
                         'Not connected user shouldn\'t be allow to get user')

        rv = self.login('admin@admin.com', 'admin')
        self.assertEqual(rv.status_code, 204, 'Login as admin Failed')

        rv = self.get_user()
        self.assertEqual(rv.status_code, 200)
        users = json.loads(rv.data)['users']
        results = User.query.all()
        self.assertEqual(len(users), len(results))

        for user, result in zip(users, results):
            self.assertEqual(user['email'], result.email)

        rv = self.get_user(user_id=1111111111)
        self.assertEqual(rv.status_code, 404)

        rv = self.get_user(user_id=1)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(User.query.get(1).email, json.loads(rv.data)['email'])

    def test_delete_user(self):
        rv = self.delete_user(user_id=2)
        self.assertEqual(rv.status_code, 401,
                         'Not connected user shouldn\'t be allow to delte user')

        rv = self.login('admin@admin.com', 'admin')
        self.assertEqual(rv.status_code, 204, 'Login as admin Failed')

        rv = self.delete_user(user_id=1111111111)
        self.assertEqual(rv.status_code, 404)

        rv = self.delete_user(user_id=2)
        self.assertEqual(rv.status_code, 204)
        self.assertIsNone(User.query.get(2))


if __name__ == '__main__':
    unittest.main()
