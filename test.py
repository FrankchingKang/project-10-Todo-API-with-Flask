# tests.py
import unittest
from models import Todo
from app import app
from peewee import SqliteDatabase


MODELS = [Todo]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class TodoTests(unittest.TestCase):

    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)
        # app.config['TESTING'] = True  # 指定app在測試模式下執行
        app.testing = True   # 指定app在測試模式下執行。 (測試模式下,檢視中的意外異常可以正常列印顯示出來)
        # 使用flask提供的測試客戶端進行測試 (Flask客戶端可以模擬傳送請求)
        self.client = app.test_client()

    # Bind the given models to the db for the duration of wrapped block.
    def use_test_database(fn):
        @wraps(fn)
        def inner(self):
            with test_db.bind_ctx(MODELS):
                test_db.create_tables(MODELS)
                try:
                    fn(self)
                finally:
                    test_db.drop_tables(MODELS)
        return inner

    def test_home_page(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_app_exist(self):
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    def test_create_item(self):
        response = self.client.post('/api/v1/todos', data=dict(
            name = "Tom"
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('name', data)

    def test_get_list_item(self):
        response = self.client.get('/api/v1/todos')
        self.assertEqual(response.status_code, 200)


    def test_404_page(self):
        response = self.client.get('/test_404')  # 传入目标 URL
        self.assertEqual(response.status_code, 404)  # 判断响应状态码


    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

        # If we wanted, we could re-bind the models to their original
        # database here. But for tests this is probably not necessary.


if __name__ == '__main__':
    unittest.main()
