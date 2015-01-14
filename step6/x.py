

class TYPE_INFO:
    TYPE_ILLEGAL = -1
    TYPE_NUMERIC = 0
    TYPE_BOOL = 1
    TYPE_STRING = 2


class SYMBOL_INFO:
    
    def __init__(self, symbol_name, type, val):

        self.symbol_name = symbol_name
        self.type = type
        self.val = val


