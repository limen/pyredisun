from redisun.vectormodel import VectorModel
from redisun.querybuilder import QueryBuilder


class SetModel(VectorModel):
    
    def _init_query_builder(self):
        self._query_builder = QueryBuilder(('class', 'id', 'members'), ('id',), ':')
        
    def create_xx(self, value, ttl=0):
        pass
    
    def create_nx(self, value, ttl=0):
        pass
    
    def update(self, value, ttl=0):
        return self.create_xx(value, ttl)
    
    def put(self, elements):
        pass
    
    def pull(self, elements):
        pass
    
    def first(self, with_ttl=False):
        pass

    def last(self, with_ttl=False):
        pass
    
    def all(self, with_ttl=False):
        pass

    def randone(self, with_ttl=False):
        pass
    
    def getset_one(self, members, ttl=0):
        pass
    
    def getset_all(self, members, ttl=0):
        pass
