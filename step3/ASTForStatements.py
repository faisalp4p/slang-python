from abc import ABCMeta, abstractmethod

class Statement:
     __metaclass__ = ABCMeta

     @abstractmethod
     def Execute(self): pass

class PrintStatement(Statement):

    def __init__(self, ex):
        self._ex = ex

    def Execute(self):
        a = self._ex.Evaluate()
        print a,
        return True

class PrintLineStatement(Statement):

    def __init__(self, ex):
        self._ex = ex

    def Execute(self):
        a = self._ex.Evaluate()
        print a
        return True
