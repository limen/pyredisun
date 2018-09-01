import unittest
from redisun.hashmodel import HashModel

class TestHashModel(unittest.TestCase):
    def setUp(self):
        self.model = HashModel()
        self.model.where_in('name',['alice','bob','cath'])

    def test_create(self):
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

#    def test_randone(self):
#        self.model.create('hiredis#2')
#        keys = self.model.keys()
#        randone = self.model.randone()
#        self.assertEquals(randone[1],'hiredis#2')
#        self.assertTrue(randone[0] in keys)
#
#    def test_get_all(self):
#        self.model.create('hiredis#3')
#        keys = self.model.keys()
#        kvs = self.model.all()
#        for k in keys:
#            self.assertTrue(k in kvs)
#            self.assertTrue(kvs[k],[k,'hiredis#3'])
#        kvs = self.model.all(True)
#        for k in keys:
#            self.assertTrue(k in kvs)
#            self.assertTrue(kvs[k],[k,'hiredis#3',-1])
#    
#    def test_create_with_ttl(self):
#        self.model.create('hiredis#4',100)
#        keys = self.model.keys()
#        kvs = self.model.all(True)
#        for k in keys:
#            self.assertTrue(k in kvs)
#            self.assertTrue(kvs[k],[k,'hiredis#4',100])
#
#    def test_create_xx(self):
#        rs = self.model.create_xx('hiredis#5')
#        for k in self.model.keys():
#            self.assertEquals(rs[k],'OK')
#
#    def test_create_nx(self):
#        rs = self.model.create_nx('hiredis#5')
#        for k in self.model.keys():
#            self.assertEquals(rs[k],None)
#
#    def test_getset_one(self):
#        self.model.remove()
#        ov = self.model.getset_one('hiredis#6')
#        self.assertTrue(ov is None)
#        ov = self.model.getset_one('hiredis#7')
#        self.assertEquals(ov, 'hiredis#6')
#        self.assertEquals(self.model.get(),'hiredis#7')
#
#    def test_getset_all(self):
#        self.model.remove()
#        keys = self.model.keys()
#        ovs = self.model.getset_all('hiredis#8')
#        self.assertEquals(len(ovs),6)
#        for i,k in enumerate(ovs):
#            self.assertTrue(k in keys)
#            self.assertTrue(ovs[k] is None)
#        return
#        ovs = self.model.getset_all('hiredis#9')
#        self.assertEquals(len(ovs),6)
#        for i,k in enumerate(ovs):
#            self.assertTrue(k in keys)
#            self.assertEquals(ovs[k], 'hiredis#8')
#        ovs = self.model.all()
#        self.assertEquals(len(ovs),6)
#        for i,k in enumerate(ovs):
#            self.assertTrue(k in keys)
#            self.assertEquals(ovs[k], 'hiredis#9')
#
#    def test_get_key_field(self):
#        key = self.model.first_key()
#        self.assertEquals(self.model.get_key_field(key,'name'),'alice')
#        self.assertEquals(self.model.get_key_field(key,'date'),'09-01')

if __name__ == '__main__':
    unittest.main()

