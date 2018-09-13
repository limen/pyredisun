from redisun.models.model import Model


class VectorModel(Model):
    
    def create_xx(self, value, ttl: int=0):
        pass
    
    def create_nx(self, value, ttl: int=0):
        pass
    
    def update(self, value, ttl: int=0):
        return self.create_xx(value, ttl)
    
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
    
    def __contains__(self, item):
        pass
    
    def __iter__(self):
        pass
    
    def __len__(self):
        pass

    def __add__(self, other):
        self.put(other)
        return self.first()
