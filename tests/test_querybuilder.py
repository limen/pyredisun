import unittest

from redisun.querybuilder import QueryBuilder


class TestQuery(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder()
    
    def test_one_field(self):
        self.qb.set_all_fields(['name'])
        self.qb.set_dynamic_fields(['name'])
        self.qb.where('name', 'alice')
        keys = self.qb.keys()
        self.assertEquals(keys, ['alice'])
        
        self.qb.where_in('name', ['alice', 'bob'])
        keys = self.qb.keys()
        self.assertEquals(keys, ['alice', 'bob'])
    
    def test_one_dynamic_field(self):
        self.qb.set_all_fields(['greeting', 'name'])
        self.qb.set_dynamic_fields(['name'])
        self.qb.set_delimiter(':')
        self.qb.where_in('name', ['alice', 'bob'])
        keys = self.qb.keys()
        self.assertEquals(keys, ['greeting:alice', 'greeting:bob'])
        
        self.qb.flush()
        self.assertEquals(self.qb.get_bindings(), {})
        keys = self.qb.keys()
        self.assertEquals(keys, [])
    
    def test_two_dynamic_fields(self):
        self.qb.set_all_fields(['greeting', 'name', 'date'])
        self.qb.set_dynamic_fields(['name', 'date'])
        self.qb.set_delimiter(':')
        self.qb.where('name', 'alice')
        self.qb.where_in('date', ['09-01', '09-02'])
        keys = self.qb.keys()
        self.assertEquals(len(keys), 2)
        self.assertEquals(keys, ['greeting:alice:09-01', 'greeting:alice:09-02'])
        
        self.qb.flush()
        self.assertEquals(self.qb.get_bindings(), {})
        keys = self.qb.keys()
        self.assertEquals(keys, [])
        
        self.qb.where('name', 'alice')
        self.qb.where_in('date', [])
        keys = self.qb.keys()
        self.assertEquals(keys, [])
    
    def test_three_dynamic_fields(self):
        self.qb.set_all_fields(['greeting', 'name', 'date', 'hour'])
        self.qb.set_dynamic_fields(['name', 'date', 'hour'])
        self.qb.set_delimiter(':')
        self.qb.where('name', 'alice')
        self.qb.where_in('date', ['09-01', '09-02'])
        self.qb.where_in('hour', ['10', '11'])
        keys = self.qb.keys()
        self.assertEquals(len(keys), 4)
        self.assertEquals(keys, ['greeting:alice:09-01:10', 'greeting:alice:09-01:11', 'greeting:alice:09-02:10',
                                 'greeting:alice:09-02:11'])
        
        self.qb.flush()
        self.assertEquals(self.qb.get_bindings(), {})
        keys = self.qb.keys()
        self.assertEquals(keys, [])
        
        self.qb.where('name', 'alice')
        self.qb.where_in('date', [])
        keys = self.qb.keys()
        self.assertEquals(keys, [])


if __name__ == '__main__':
    unittest.main()
