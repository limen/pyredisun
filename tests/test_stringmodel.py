import unittest

from redisun.models.stringmodel import StringModel
from redisun.utils import *


class TestStringModel(unittest.TestCase):
    def setUp(self):
        self.model = StringModel()
        self.model.where_in('name', ['alice', 'bob', 'cath']).where_in('date', ['09-01', '09-02'])
        self.value = 'hello human-being'
    
    def test_create(self):
        keys = self.model.keys()
        self.assertEqual(len(keys), 6)
        (ok_keys, ok_keys_value, _, _) = self.model.create('hello-world')
        self.assertEqual(len(keys), len(ok_keys))
        self.assertEqual([k for k in keys if k not in ok_keys], [])
        (ok_keys, ok_keys_value, _, _) = self.model.all()
        for k in keys:
            self.assertEqual(ok_keys_value[k], 'hello-world')
    
    def test_remove(self):
        keys = self.model.keys()
        self.model.create('hello-world')
        self.assertEqual(self.model.remove(), len(keys))
        (ok_keys, ok_keys_value, _, _) = self.model.all()
        for k in keys:
            self.assertTrue(ok_keys_value[k] is None)
    
    def test_first(self):
        self.model.create('hiredis')
        first = self.model.first()
        if first is not None:
            first_key, first_value = first
            self.assertTrue(first_key in self.model.keys())
            self.assertEqual(first_value, 'hiredis')

        self.model.remove()
        first = self.model.first()
        self.assertEqual(first, None)
    
    def test_last(self):
        self.model.create('hiredis#1')
        keys = self.model.keys()
        last = self.model.last()
        if last is not None:
            last_key, last_value = last
            self.assertTrue(last_key == keys[len(keys) - 1])
            self.assertTrue(last_value == 'hiredis#1')
        self.model.where('name', 'cath').where('date', '09-02').delete()
        self.model.where_in('name', ['alice', 'bob', 'cath']).where_in('date', ['09-01', '09-02'])
        last_key, last_value = self.model.last()
        self.assertEqual(last_key, keys[len(keys) - 2])
        self.assertEqual(last_value, 'hiredis#1')
    
    def test_randone(self):
        self.model.create('hiredis#2')
        keys = self.model.keys()
        rand_key, rand_value = self.model.randone()
        self.assertEqual(rand_value, 'hiredis#2')
        self.assertTrue(rand_key in keys)
    
    def test_get_all(self):
        self.model.create('hiredis#3')
        keys = self.model.keys()
        ok_keys, ok_keys_value, _, _ = self.model.all()
        for k in keys:
            self.assertTrue(k in ok_keys)
            self.assertTrue(ok_keys_value[k], 'hiredis#3')
        ok_keys, ok_keys_value, _, _ = self.model.all(True)
        for k in keys:
            self.assertTrue(k in ok_keys)
            self.assertTrue(ok_keys_value[k], ['hiredis#3', -1])
    
    def test_create_with_ttl(self):
        self.model.create('hiredis#4', 100)
        keys = self.model.keys()
        ok_keys, ok_keys_value, _, _ = self.model.all(True)
        for k in keys:
            self.assertTrue(k in ok_keys)
            self.assertTrue(ok_keys_value[k], ['hiredis#4', 100])
    
    def test_create_xx(self):
        self.model.create('hiredis#5')
        ok_keys, ok_keys_value, _, _ = self.model.create_xx('hiredis#5')
        for k in self.model.keys():
            self.assertEqual(ok_keys_value[k], 'OK')
        self.model.remove()
        ok_keys, ok_keys_value, failed_keys_status, _ = self.model.create_xx('hiredis#5')
        self.assertEqual(len(ok_keys), 0)
        self.assertEqual(len(failed_keys_status), len(self.model.keys()))
        for k in self.model.keys():
            self.assertEqual(failed_keys_status[k], STATUS_EXISTENCE_NOT_SATISFIED)
    
    def test_create_nx(self):
        self.model.remove()
        ok_keys, ok_keys_value, _, _ = self.model.create_nx('hiredis#6')
        for k in self.model.keys():
            self.assertEqual(ok_keys_value[k], 'OK')
        self.model.create('hiredis#6')
        ok_keys, ok_keys_value, failed_keys_status, _ = self.model.create_nx('hiredis#6')
        self.assertEqual(len(ok_keys), 0)
        self.assertEqual(len(failed_keys_status), len(self.model.keys()))
        for k in self.model.keys():
            self.assertEqual(failed_keys_status[k], STATUS_EXISTENCE_NOT_SATISFIED)
    
    def test_getset_one(self):
        self.model.remove()
        key, status, value, _ = self.model.getset_one('hiredis#6')
        self.assertTrue(value is None)
        key, status, value, _ = self.model.getset_one('hiredis#7', 300)
        self.assertEqual(value, 'hiredis#6')
        k, v, ttl = self.model.first(True)
        self.assertEqual(v, 'hiredis#7')
        self.assertEqual(ttl, 300)
    
    def test_getset_all(self):
        self.model.remove()
        keys = self.model.keys()
        ok_keys, ok_keys_value, failed_keys_status, failed_keys_hint = self.model.getset_all('hiredis#8')
        self.assertEqual(len(ok_keys), 6)
        for k in ok_keys:
            self.assertTrue(k in keys)
            self.assertTrue(ok_keys_value[k] is None)
        ok_keys, ok_keys_value, failed_keys_status, failed_keys_hint = self.model.getset_all('hiredis#9')
        self.assertEqual(len(ok_keys), 6)
        for k in ok_keys:
            self.assertTrue(k in keys)
            self.assertEqual(ok_keys_value[k], 'hiredis#8')
        ok_keys, ok_keys_value, failed_keys_status, failed_keys_hint = self.model.all()
        self.assertEqual(len(ok_keys), 6)
        for k in ok_keys:
            self.assertTrue(k in keys)
            self.assertEqual(ok_keys_value[k], 'hiredis#9')

    def test_ttl(self):
        self.model.remove()
        self.model.create('hiredis#10', 100)
        key, value, ttl = self.model.first(True)
        self.assertEqual(value, 'hiredis#10')
        self.assertEqual(ttl, 100)
    
    def test_get_key_field(self):
        key = self.model.first_key()
        self.assertEqual(self.model.get_key_field(key, 'name'), 'alice')
        self.assertEqual(self.model.get_key_field(key, 'date'), '09-01')


if __name__ == '__main__':
    unittest.main()
