from redisun.models.vectormodel import VectorModel
from redisun.querybuilder import QueryBuilder


class SortedSetModel(VectorModel):
    
    def _init_query_builder(self):
        self._query_builder = QueryBuilder(('area', 'id', 'candidates'), ('id',), ':')
    
    def create_xx(self, value: dict, ttl=0):
        pass
    
    def create_nx(self, value: dict, ttl=0):
        pass
    
    def update(self, value: dict, ttl=0):
        return self.create_xx(value, ttl)
    
    def put(self, elements: dict):
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
    
    def getset_one(self, members: dict, ttl: int=0):
        pass
    
    def getset_all(self, members: dict, ttl: int=0):
        pass
