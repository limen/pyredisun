from itertools import product
from random import randint


class QueryBuilder(object):
    """ Build query keys
    The key should be of style like 'greeting:alice:09-01'.
    which has three fields at all and two dynamic fields.
    The fields are joined by a delimiter like ':'.

    All fields: greeting, <name>, <date>
    Dynamic fields: <name>, <date>

    One can bind values to dynamic field use method where/where_in. 

    ## Notice ##
    The keys's field name should be unique or there would be unexpected result
    
    ## Usage ## 
    qb = QueryBuilder(['greeting','name','date'], ['name','date'], ':')
    qb.where_in('name', ['alice', 'bob'])
    qb.where_in('date', ['09-01', '09-02', '09-03'])
    qb.keys()
    
    ## Result ##
    ['greeting:alice:09-01', 'greeting:alice:09-02', 'greeting:alice:09-03',
    'greeting:bob:09-01', 'greeting:bob:09-02', 'greeting:bob:09-03']

    Tested Python versions
    - 3.6.5
    - 2.7.5

    """
    
    def __init__(self, all_fields=(), dynamic_fields=(), delimiter='', bindings=None):
        self._all_fields = all_fields
        self._dynamic_fields = dynamic_fields
        self._delimiter = delimiter
        self._bindings = dict(bindings)
        self._cached_keys = None
    
    def set_all_fields(self, fields):
        self._all_fields = fields
        return self
    
    def set_dynamic_fields(self, fields):
        self._dynamic_fields = fields
        return self
    
    def set_delimiter(self, delim):
        self._delimiter = delim
        return self
    
    def get_all_fields(self):
        return self._all_fields
    
    def get_dynamic_fields(self):
        return self._dynamic_fields
    
    def get_delimiter(self):
        return self._delimiter
    
    def where(self, field, value):
        """ Bind value to a dynamic field.
        The value should be a string.
        """
        self._bind_one(field, value)
        self._clean_cached_keys()
        return self
    
    def where_in(self, field, values):
        """ Bind values to a dynamic field.
        The values should be a tuple/list which holds strings only.
        """
        self._bind_multi(field, values)
        self._clean_cached_keys()
        return self
    
    def get_bindings(self):
        return self._bindings
    
    def get_field(self, key, field):
        parts = key.split(self.get_delimiter())
        all_fields = self.get_all_fields()
        if field in all_fields:
            return parts[all_fields.index(field)]
        return None
    
    def flush(self):
        """ Flush the bingdings.
        Do it before starting a new query.
        """
        self._bindings = {}
        self._cached_keys = None
    
    def first_key(self):
        keys = self.keys()
        return keys[0] if len(keys) > 0 else None
    
    def last_key(self):
        keys = self.keys()
        return keys[len(keys) - 1] if len(keys) > 0 else None
    
    def random_key(self):
        keys = self.keys()
        return keys[randint(0, len(keys) - 1)] if len(keys) > 0 else None
    
    def keys(self):
        return self._compose_keys()
    
    def _compose_keys(self):
        """ compose query keys
        """
        if self._cached_keys is not None:
            return self._cached_keys
        keys = []
        binding_rows = self._combine_bindings()
        all_fields = self.get_all_fields()
        dynamic_fields = self.get_dynamic_fields()
        for row in binding_rows:
            row.reverse()
            parts = []
            for i, k in enumerate(all_fields):
                parts += [k] if k not in dynamic_fields else [row.pop()]
            keys += [self.get_delimiter().join(parts)]
        self._cache_keys(keys)
        return keys
    
    def _combine_bindings(self):
        """ Explain bindings to rows
        e.g. {name:('alice','bob'), date:('09-01','09-02', '09-03')}
        would be explain to
        [
            ['alice','09-01'],
            ['alice','09-02'],
            ['alice','09-03'],
            ['bob','09-01'],
            ['bob','09-02'],
            ['bob','09-03'],
        ]
        """
        rows = []
        binds = self.get_bindings()
        if not binds:
            return rows
        
        # take example above, its field ranges would be 
        # [[0,1], [0,1,2]]
        field_ranges = []
        dynamic_fields = self.get_dynamic_fields()
        for field in dynamic_fields:
            values = binds.get(field)
            if values is None:
                return rows
            else:
                field_ranges += [list(range(len(values)))]
        # take example above, its field index combination would be 
        # [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2]]
        # each element tells the index of the binding value
        field_index_combination = list(product(*field_ranges))
        for field_indexes in field_index_combination:
            field_indexes = list(field_indexes)
            row = []
            for index, field in enumerate(dynamic_fields):
                row += [binds.get(field)[field_indexes[index]]]
            rows += [row]
        return rows
    
    def _cache_keys(self, keys):
        self._cached_keys = keys
    
    def _clean_cached_keys(self):
        self._cached_keys = None
    
    def _bind_one(self, field, value):
        if not isinstance(value, str):
            raise TypeError('The value to bind should be str type, %s given' % type(value))
        self._bindings[field] = (value,)
    
    def _bind_multi(self, field, values):
        if not isinstance(values, list):
            raise TypeError('The values to bind should be list type, %s given' % type(values))
        else:
            for elem in values:
                if not isinstance(elem, str):
                    raise TypeError('Each of the values should be str type, %s given' % type(elem))
        self._bindings[field] = values
