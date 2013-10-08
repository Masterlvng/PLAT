import unittest

from app import app, db
from app.models import User, ROLE_ADMIN

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:masterlvng@localhost/plat_test'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_Login(self):
        u = User(nickname='masterlvng',password='123456',email='masterlvng@gmail.com',\
                role=ROLE_ADMIN)
        db.session.add(u)
        db.session.commit()
        assert u.id == 1
        rv1 = self.app.post('/login',data=dict(
                account='masterlvng',
                password='123456'
            ),follow_redirects=False)
        assert 'success' in rv1.data
        rv2 = self.app.post('/login')
        assert 'logined' in rv2.data


if __name__ == '__main__':
    unittest.main()
