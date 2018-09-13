import unittest

from redisun.models.hashmodel import HashModel
from redisun.utils import *


class TestHashModel(unittest.TestCase):
    def setUp(self):
        self.model = HashModel()
        self.model.where_in('name', ['alice', 'bob', 'cath'])
    
    def test_create(self):
        self.model.remove()
        keys = self.model.keys()
        self.assertEqual(len(keys), 3)
        ok_keys, ok_keys_value, _, _ = self.model.create({'age': '22'})
        self.assertEqual(len(keys), len(ok_keys))
        self.assertEqual([k for k in keys if k not in ok_keys], [])
        ok_keys, ok_keys_value, _, _ = self.model.all()
        for k in keys:
            self.assertEqual(ok_keys_value[k], {'age': '22'})
    
    def test_remove(self):
        keys = self.model.keys()
        self.model.create({'name': '22'})
        self.assertEqual(self.model.remove(), len(keys))
        ok_keys, ok_keys_value, _, _ = self.model.all()
        for k in keys:
            self.assertTrue(k not in ok_keys)
    
    def test_first(self):
        self.model.remove()
        self.model.create({'age': '22'})
        first = self.model.first()
        if first is not None:
            first_key, first_value = first
            self.assertEqual(first_value, {'age': '22'})
            self.assertEqual(first_key, self.model.first_key())
        self.model.delete()
        first = self.model.first()
        if first is not None:
            first_key, first_value = first
            self.assertEqual(first_value, {'age': '22'})
            self.assertEqual(first_key, self.model.keys()[1])
    
    def test_last(self):
        value = {'age': '23'}
        self.model.create(value)
        keys = self.model.keys()
        last_key, last_value = self.model.last()
        self.assertEqual(last_key, keys[len(keys) - 1])
        self.assertEqual(last_value, value)
        self.model.where('name', 'cath').delete()
        self.model.where_in('name', ['alice', 'bob', 'cath'])
        last_key, last_value = self.model.last()
        self.assertEqual(last_key, keys[len(keys) - 2])
        self.assertEqual(last_value, value)
    
    def test_randone(self):
        value = {'age': '24'}
        self.model.create(value)
        keys = self.model.keys()
        rand_key, rand_value = self.model.randone()
        self.assertEqual(rand_value['age'], value['age'])
        self.assertTrue(rand_key in keys)
    
    def test_get_all(self):
        value = {'age': 25, 'address': 'ca'}
        self.model.create(value)
        keys = self.model.keys()
        ok_keys, ok_keys_value, _, _ = self.model.all()
        for k in keys:
            self.assertTrue(k in ok_keys)
            self.assertTrue(ok_keys_value[k], value)
        ok_keys, ok_keys_value, _, _ = self.model.all([], True)
        for k in keys:
            self.assertTrue(k in ok_keys_value)
            self.assertTrue(ok_keys_value[k], [value, -1])
    
    def test_create_with_ttl(self):
        value = {'age': '25', 'address': 'caa'}
        self.model.create(value, 100)
        keys = self.model.keys()
        ok_keys, ok_keys_value, _, _ = self.model.all([], True)
        for k in keys:
            self.assertTrue(k in ok_keys)
            self.assertTrue(ok_keys_value[k], [value, 100])
    
    def test_create_xx(self):
        value = {'age': 27, 'address': 'caa'}
        self.model.create(value)
        ok_keys, ok_keys_value, _, _ = self.model.create_xx(value)
        for k in self.model.keys():
            self.assertEqual(ok_keys_value[k], 'OK')
        self.model.remove()
        ok_keys, _, failed_keys_status, _ = self.model.create_xx(value)
        self.assertEqual(len(ok_keys), 0)
        for k in self.model.keys():
            self.assertEqual(failed_keys_status[k], STATUS_EXISTENCE_NOT_SATISFIED)
    
    def test_create_nx(self):
        value = {'age': 27, 'address': 'caa'}
        self.model.remove()
        ok_keys, ok_keys_value, _, _ = self.model.create_nx(value)
        self.assertEqual(len(ok_keys), len(self.model.keys()))
        for k in self.model.keys():
            self.assertEqual(ok_keys_value[k], 'OK')
        self.model.create(value)
        ok_keys, _, failed_keys_status, _ = self.model.create_nx(value)
        self.assertEqual(len(ok_keys), 0)
        for k in self.model.keys():
            self.assertEqual(failed_keys_status[k], STATUS_EXISTENCE_NOT_SATISFIED)
    
    def test_getset_one(self):
        self.model.remove()
        value = {'age': '27', 'address': 'caa'}
        key, status, old_value, _ = self.model.getset_one(value)
        first_key = self.model.first_key()
        self.assertEqual(key, first_key)
        self.assertTrue(old_value is None)
        self.assertEqual(status, STATUS_OK)
        value1 = {'age': '28', 'address': 'caa'}
        first_key, status, old_value, _ = self.model.getset_one(value1, [], 300)
        self.assertEqual(old_value, value)
        self.assertEqual(self.model.first([], True), [first_key, value1, 300])
        self.assertEqual(self.model.first(['age']), [first_key, {'age': '28'}])
    
    def test_getset_all(self):
        self.model.remove()
        keys = self.model.keys()
        value = {'age': '19', 'address': 'ca'}
        ok_keys, ok_keys_value, _, _ = self.model.getset_all(value)
        self.assertEqual(len(ok_keys), 3)
        for k in keys:
            self.assertTrue(k in ok_keys_value)
            self.assertTrue(ok_keys_value[k] is None)
        ok_keys, ok_keys_value, _, _ = self.model.all()
        self.assertEqual(len(ok_keys), 3)
        for k in ok_keys:
            self.assertTrue(k in keys)
            self.assertEqual(ok_keys_value[k], value)

    def test_ttl(self):
        self.model.remove()
        value = {'age': '19', 'address': 'ca'}
        self.model.create(value, 100)
        key, val, ttl = self.model.first([], True)
        self.assertEqual(val, value)
        self.assertEqual(ttl, 100)


if __name__ == '__main__':
    unittest.main()
