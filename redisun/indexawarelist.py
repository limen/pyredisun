
class IndexAwareList(object):
    """
    List has awareness of its index bound
    """
    def __init__(self, lt: list):
        self._list = lt
        
    def __getitem__(self, item):
        if len(self._list) > item:
            return self._list[item]
        return None
