import unittest

from flask import json

from app.core import app
from app.model import USER, user_class, GROUP, group_class


class GroupTestCase(unittest.TestCase):
    uid = None
    uid2 = None

    @classmethod
    def setUpClass(cls):
        query = USER.insert().values(email="admin@admin.com", role="4", phone="00.00.00.00.00", name="admin",
                                     hash="toto")
        res = query.execute()
        cls.uid = res.lastrowid
        query = USER.insert().values(email="adminx@admin.com", role="3", phone="00.00.00.00.00", name="adminx",
                                     hash="zozo")
        res = query.execute()
        cls.uid2 = res.lastrowid

    @classmethod
    def tearDownClass(cls):
        query = GROUP.delete().where(group_class.name == "group_test")
        query.execute()
        query = GROUP.delete().where(group_class.name == "group_test2")
        query.execute()
        query = USER.delete().where(user_class.email == "admin@admin.com")
        query.execute()
        query = USER.delete().where(user_class.email == "adminx@admin.com")
        query.execute()

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def create_group(self, name, year, class_short, class_long, department, resp_id, sec_id):
        return self.app.post('/api/group',
                             data=json.dumps(
                                 dict(
                                     name=name,
                                     year=year,
                                     class_short=class_short,
                                     class_long=class_long,
                                     department=department,
                                     resp_id=resp_id,
                                     sec_id=sec_id
                                 )
                             ), content_type='application/json')

    def getGroupByID(self, GID):
        return self.app.get('/api/group/bygid/' + str(GID))

    def getGroupByName(self, name):
        return self.app.get('/api/group/byname/' + name)

    def change_group(self, GID, name, year, class_short, class_long, department, resp_id, sec_id):
        return self.app.put('/api/group/bygid/' + str(GID),
                            data=json.dumps(
                                dict(
                                    name=name,
                                    year=year,
                                    class_short=class_short,
                                    class_long=class_long,
                                    department=department,
                                    resp_id=resp_id,
                                    sec_id=sec_id
                                )
                            ), content_type='application/json')

    def test_group(self):
        rv = self.create_group('group_test', '2017', 'GT', 'GROUP_TEST', 'TESTING', self.uid, self.uid2)
        self.assertEqual(rv.status_code, 201, 'Creating group Failed')
        gid = json.loads(rv.data)['GID']
        self.assertIsNotNone(gid)

        rv = self.create_group('group_test', '2017', 'GT', 'GROUP_TEST', 'TESTING', self.uid, self.uid2)
        self.assertEqual(rv.status_code, 200, 'Group is supposed to already exist')
        gid2 = json.loads(rv.data)['GID']
        self.assertEqual(gid, gid2, "The GID must be the same !")

        rv = self.getGroupByID(gid)
        self.assertEqual(rv.status_code, 200, 'Getting group failed by ID')
        group = json.loads(rv.data)['GROUP']
        self.assertIsNotNone(group)

        rv = self.getGroupByName("group_test")
        self.assertEqual(rv.status_code, 200, 'Getting group failed by Name')
        group2 = json.loads(rv.data)['GROUP']
        self.assertEqual(group, group2, "Group by name must be the same !")

        rv = self.change_group(gid, 'group_test2', '2018', 'GT2', 'GROUP_TEST2', 'TESTING2', self.uid2, self.uid)
        self.assertEqual(rv.status_code, 200, 'Group modification failed !')
        gid3 = json.loads(rv.data)['GID']
        self.assertEqual(gid, gid3, "GIDs doesn't match !")

        rv = self.getGroupByName('group_test2')
        self.assertEqual(rv.status_code, 200, 'Getting modified group failed by Name')
        group4 = json.loads(rv.data)['GROUP']
        self.assertIsNotNone(group4, "Modified group shouldn't be None !")


if __name__ == '__main__':
    unittest.main()
