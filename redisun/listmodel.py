from redisun.vectormodel import VectorModel
from redisun.querybuilder import QueryBuilder


class ListModel(VectorModel):
    
    def _init_query_builder(self):
        self._query_builder = QueryBuilder(('queue', 'id', 'messages'), ('id',), ':')
    
    def create_xx(self, elements, ttl: int=0):
        pass
    
    def create_nx(self, elements, ttl: int=0):
        pass
    
    def update(self, elements, ttl: int=0):
        return self.create_xx(elements, ttl)
    
    def put(self, elements):
        pass
    
    def pull(self, elements):
        pass
    
    def first(self, with_ttl: bool=False):
        pass
    
    def last(self, with_ttl: bool=False):
        pass
    
    def all(self, with_ttl: bool=False):
        pass
    
    def randone(self, with_ttl: bool=False):
        pass
    
    def getset_one(self, members, ttl: int=0):
        pass
    
    def getset_all(self, members, ttl: int=0):
        pass
