import unittest
from StringIO import StringIO
from app import app, db
from app.models import User, ROLE_ADMIN,ROLE_OFFICIAL, Annoucement
import json

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:masterlvng@localhost/plat_test'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_Login(self):
        u = User(nickname='masterlvng',password='123456',email='masterlvng@gmail.com',\
                role=ROLE_OFFICIAL)
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

    def test_Issue_Ann(self):
        self.test_Login()
        with open('arch.jpg') as f:
            poster = StringIO(f.read())
        with open('form.doc') as f:
            form = StringIO(f.read())
        rv = self.app.post('/issue/annoucement',data=dict(
                name='weinasi',
                topic="vernas",
                summary="good show",
                poster=(poster,'arch.jpg'),
                addr="xiongdelong",
                sdate="2013-8-20",
                scope=1,
                host="gbt",
                undertaker="gbt2",
                sponsor="donggandidai",
                form=(form,'form.doc'),
                contact="qq=370378348",
                qna="hehe",
                accept_apply=1,
                user_id=1
            ))
        assert 'success' in rv.data

    def test_Dis_Annoucement(self):
        self.test_Issue_Ann()
        rv = self.app.get('/masterlvng/weinasi')
        print rv.data

    def test_Mod_Annoucement(self):
        self.test_Issue_Ann()
        rv = self.app.post('/masterlvng/weinasi',data=dict(
                Mod_content='{"addr":"yingdong"}'
            ))
        assert 'mod' in rv.data
        rv1 = self.app.get('/masterlvng/weinasi')

    def test_Mod_Form(self):
        self.test_Issue_Ann()
        with open('Form2.doc') as f:
            form = StringIO(f.read())
        rv = self.app.post('/mod/form/weinasi',data=dict(\
                form=(form,'Form2.doc')
            ))
        print rv.data
        assert 'success' in rv.data

    def test_Apply(self):
        self.test_Issue_Ann()
        with open('Zhangliangfu.doc') as f:
            form = StringIO(f.read())
        rv = self.app.post('/apply/masterlvng/weinasi',data=dict(\
            name='zhangliangfu',
            sex=0,
            contact="qq=370378348",
            form=(form,'zhangliangfu.doc')
            ))
        print rv.data
        assert 'suc' in rv.data

    def test_down_forms(self):
        self.test_Issue_Ann()
        rv = self.app.get('/forms/masterlvng/weinasi')
        print rv.data

    def test_stat_forms(self):
        self.test_Apply()
        rv = self.app.get('/statistics/masterlvng/weinasi')
        print rv.data

    def test_User_Anns(self):
        self.test_Issue_Ann()
        rv = self.app.post('/masterlvng',data=dict(
                start=0,
                offset=2
            ))
        print rv.data

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestCase('test_User_Anns'))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
