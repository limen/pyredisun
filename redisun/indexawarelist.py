
class IndexAwareList(list):
    """
    List has awareness of its index bound
    """
    
    def __getitem__(self, item):
        if len(self) > item:
            return super(IndexAwareList, self).__getitem__(item)
        return None
