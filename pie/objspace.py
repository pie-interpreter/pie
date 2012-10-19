from operator import add
from pie.objects.intobject import W_IntObject

__author__ = 'sery0ga'

class ObjSpace(object):

    def plus(self, left, right):
        return W_IntObject(add(left.intval,right.intval))