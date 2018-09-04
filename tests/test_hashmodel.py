import unittest
from redisun.hashmodel import HashModel

class TestHashModel(unittest.TestCase):
    def setUp(self):
        self.model = HashModel()
        self.model.where_in('name',['alice','bob','cath'])

    def test_create(self):
        self.model.remove()
        keys = self.model.keys()
        self.assertEquals(len(keys),3)
        rs = self.model.create({'age':'22'})
        self.assertEquals(len(keys),len(rs))
        self.assertEquals([k for k in keys if k not in rs],[])
        kvs = self.model.all()
        for k in keys:
            self.assertEquals(kvs[k],{'age':'22'})
    
    def test_remove(self):
        keys = self.model.keys()
        self.model.create({'name':'22'})
        self.assertEquals(self.model.remove(),len(keys))
        kvs = self.model.all()
        for k in keys:
            self.assertTrue(k not in kvs)

    def test_first(self):
        self.model.create({'age':'22'})
        first = self.model.first()
        self.assertEquals(first,[self.model.keys()[0],{'age':'22'}])
        self.model.delete()
        first = self.model.first()
        self.assertEquals(first,[self.model.keys()[1],{'age':'22'}])

    def test_last(self):
        value = {'age':'23'}
        self.model.create(value)
        keys = self.model.keys()
        last = self.model.last()
        self.assertEquals(last,[keys[len(keys)-1],value])
        self.model.where('name','cath').delete()
        self.model.where_in('name',['alice','bob','cath'])
        last = self.model.last()
        self.assertEquals(last,[keys[len(keys)-2],value])

    def test_randone(self):
        value = {'age':'24'}
        self.model.create(value)
        keys = self.model.keys()
        randone = self.model.randone()
        self.assertEquals(randone[1]['age'], value['age'])
        self.assertTrue(randone[0] in keys)

    def test_get_all(self):
        value = {'age':25,'address':'ca'}
        self.model.create(value)
        keys = self.model.keys()
        kvs = self.model.all()
        for k in keys:
            self.assertTrue(k in kvs)
            self.assertTrue(kvs[k],[k, value])
        kvs = self.model.all([],True)
        for k in keys:
            self.assertTrue(k in kvs)
            self.assertTrue(kvs[k],[k, value, -1])
    
    def test_create_with_ttl(self):
        value = {'age':'25', 'address':'caa'}
        self.model.create(value,100)
        keys = self.model.keys()
        kvs = self.model.all([],True)
        for k in keys:
            self.assertTrue(k in kvs)
            self.assertTrue(kvs[k],[k,value,100])

    def test_create_xx(self):
        value = {'age':27, 'address':'caa'}
        self.model.create(value)
        rs = self.model.create_xx(value)
        for k in self.model.keys():
            self.assertEquals(rs[k], 'OK')
        self.model.remove()
        rs = self.model.create_xx(value)
        for k in self.model.keys():
            self.assertNotEquals(rs[k], 'OK')

    def test_create_nx(self):
        value = {'age':27, 'address':'caa'}
        self.model.remove()
        rs = self.model.create_nx(value)
        for k in self.model.keys():
            self.assertEquals(rs[k], 'OK')
        self.model.create(value)
        rs = self.model.create_nx(value)
        for k in self.model.keys():
            self.assertNotEquals(rs[k], 'OK')

    def test_getset_one(self):
        self.model.remove()
        value = {'age':'27', 'address':'caa'}
        ov = self.model.getset_one(value)
        first_key = self.model.first_key()
        self.assertTrue(bool(ov[first_key]) is False)
        value1 = {'age':'28', 'address':'caa'}
        ov = self.model.getset_one(value1)
        self.assertEquals(ov[first_key], value)
        self.assertEquals(self.model.first(),[first_key, value1])

    def test_getset_all(self):
        self.model.remove()
        keys = self.model.keys()
        value = {'age': '19', 'address':'ca'}
        ovs = self.model.getset_all(value)
        self.assertEquals(len(ovs),3)
        for i,k in enumerate(ovs):
            self.assertTrue(k in keys)
            self.assertTrue(bool(ovs[k]) is False)
        ovs = self.model.all()
        self.assertEquals(len(ovs),3)
        for i,k in enumerate(ovs):
            self.assertTrue(k in keys)
            self.assertEquals(ovs[k], value)

if __name__ == '__main__':
    unittest.main()
