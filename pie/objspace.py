from pie.objects.conststring import W_ConstStringObject
from pie.objects.int import W_IntObject

__author__ = 'sery0ga'

class ObjSpace(object):

    def plus(self, left, right):
        return W_IntObject(str(left.intval + right.intval))

    def minus(self, left, right):
        return W_IntObject(str(left.intval - right.intval))

    def multiply(self, left, right):
        return W_IntObject(str(left.intval*right.intval))

    def int(self, value):
        return W_IntObject(str(value))

    def str(self, value):
        return W_ConstStringObject(value)