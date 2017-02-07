try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
from flask_testing import TestCase
import json
from manager import app, db
from src import configs
from src.user.models import User, Role, UserRole
from src.user.schemas import UserSchema, RoleSchema


class TestSetup(TestCase):

    def create_app(self):
        # pass in test configuration
        return app

    def setUp(self):
        config = configs.get('testing')
        app.config.from_object(config)
        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def test_setup(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)


class TestUser(TestSetup):

    def test_delete_users(self):
        users = User.query.all()
        for user in users:
            db.session.delete(user)
            db.session.commit()
        self.assert404(self.client.get("/test/v1/user/"))

    def test_add_users(self):

        for i in range(0, 10):
            data = {'email': str(i)+'_saurabh@gmail.com', 'password': '123', 'username': 'saurabh_'+str(i)}
            user, error = UserSchema().load(data, session=db.session)
            self.assertEqual(error, {}, 'no errors')
            db.session.add(user)
            db.session.commit()

        self.assert200(self.client.get("/test/v1/user/"), 200)

    def test_user_api(self):

        response = self.client.post("/test/v1/user/", data=json.dumps({'username': 'sa1', 'email': 'sa@g.com',
                                                                       'password': '12121212'}),
                                    headers={'Content-Type': 'application/json'})

        self.assertEqual(response.status, '201 CREATED')
        user_id = response.json['data'][0]['id']
        self.assert200(self.client.get('/test/v1/user/'+str(user_id)+'/'), 'user found')

        self.assertEqual(self.client.delete('/test/v1/user/'+str(user_id)+'/').status, '204 NO CONTENT')


class TestRole(TestSetup):

    def test_delete_users(self):
        roles = Role.query.all()
        for role in roles:
            db.session.delete(role)
            db.session.commit()
        self.assert404(self.client.get("/test/v1/role/"))

    def test_add_roles(self):

        for i in range(0, 10):
            data = {'name': 'admin_'+str(i)}
            role, error = RoleSchema().load(data, session=db.session)
            self.assertEqual(error, {}, 'no errors')
            db.session.add(role)
            db.session.commit()

        self.assert200(self.client.get("/test/v1/role/"), 200)

    def test_role_api(self):

        response = self.client.post("/test/v1/role/", data=json.dumps({'name': 'admin_a'}),
                                    headers={'Content-Type': 'application/json'})

        self.assertEqual(response.status, '201 CREATED')
        role_id = response.json['data'][0]['id']
        self.assert200(self.client.get('/test/v1/role/'+str(role_id)+'/'), 'role found')

        self.assertEqual(self.client.delete('/test/v1/role/'+str(role_id)+'/').status, '204 NO CONTENT')


class TestUserRole(TestSetup):

    def test_delete_users(self):
        roles = UserRole.query.all()
        for role in roles:
            db.session.delete(role)
            db.session.commit()
        self.assertEqual(UserRole.query.all(), [])

    def test_role_api(self):
        user = User()
        user.username = '1'
        user.email = '1@1.com'
        user.password = '123'
        db.session.add(user)
        role = Role()
        role.name = '1'
        db.session.add(role)
        db.session.commit()
        response = self.client.patch("/test/v1/user_role/",
                                     data=json.dumps([
                                         {
                                             '__action': 'add',
                                             'user_id': user.id,
                                             'role_id': role.id
                                         },
                                         {
                                             '__action': 'remove',
                                             'user_id': user.id,
                                             'role_id': role.id
                                         },
                                         {
                                             '__action': 'add',
                                             'user_id': user.id,
                                             'role_id': role.id
                                         },
                                         {
                                             '__action': 'remove',
                                             'user_id': user.id,
                                             'role_id': role.id
                                         }
                                     ]),
                                     headers={'Content-Type': 'application/json'})

        self.assertEqual(response.status, '200 OK')

        response = self.client.patch("/test/v1/user_role/",
                                     data=json.dumps([
                                         {
                                             '__action': 'add',
                                             'user_id': user.id,
                                             'role_id': role.id
                                         },
                                         {
                                             '__action': 'add',
                                             'user_id': user.id,
                                             'role_id': role.id
                                         }
                                     ]),
                                     headers={'Content-Type': 'application/json'})

        self.assertEqual(response.status, '400 BAD REQUEST')


class TestSetupFailure(TestCase):

    def _pre_setup(self):
        pass

    def test_setup_failure(self):
        """Should not fail in _post_teardown if _pre_setup fails"""

        assert True
