import json

from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(json.loads(response.data),
                                     {'name': 'test', 'id': 1, 'items': []})

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(
                    json.loads(response.data),
                    {'message': "A store with name 'test' already exists."}
                )

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.delete('/store/test')

                self.assertEqual(response.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name('test'))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.get('/store/test')

                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(
                    json.loads(response.data),
                    {'name': 'test', 'id': 1, 'items': []})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/test')

                self.assertEqual(response.status_code, 404)
                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'Store not found'})

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                client.post('/item/test_item',
                            data={'price': 19.99, 'store_id': 1})
                response = client.get('/store/test')

                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(
                    json.loads(response.data),
                    {'name': 'test', 'id': 1, 'items': [
                        {'name': 'test_item', 'price': 19.99}
                    ]})

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    json.loads(response.data), {'stores': []})


    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    json.loads(response.data),
                    {'stores': [{'name': 'test', 'id': 1, 'items': []}]})