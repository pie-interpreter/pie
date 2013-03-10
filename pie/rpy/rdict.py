from rpython.rtyper.extregistry import ExtRegistryEntry
from rpython.annotator import model as annmodel
from rpython.tool.pairtype import pairtype
from rpython.rtyper.lltypesystem import lltype
from rpython.rtyper.lltypesystem.rstr import STR, StringRepr
from rpython.rtyper.rmodel import Repr
from rpython.rtyper.rint import IntegerRepr
from hippy.rpy import lldict
from collections import OrderedDict


class Iterator(object):
    def __init__(self, d):
        self.i = iter(d)
        self.d = d

    def next(self):
        k = self.i.next()
        return self.d[k]

    def nextitem(self):
        k = self.i.next()
        return (k, self.d[k])


class RDict(object):
    def __init__(self, value_cls):
        self.d = OrderedDict()
        self.value_cls = value_cls

    def __getitem__(self, item):
        return self.d[self._key(item)]

    def __setitem__(self, item, value):
        self.d[self._key(item)] = value

    def __delitem__(self, item):
        del self.d[item]   # xxx?  what about iterators

    def __len__(self):
        return len(self.d)

    def copy(self):
        cp = RDict(self.value_cls)
        cp.d = self.d.copy()
        return cp

    def __contains__(self, item):
        return self._key(item) in self.d

    def iter(self):
        return Iterator(self.d)

    def _key(self, item):
        if isinstance(item, str):
            return item
        elif isinstance(item, list):
            return "".join(item)
        else:
            assert isinstance(item, int)
            return str(item)

    def reverse(self, preserve):
        _copy = self.copy()
        _items = _copy.d.items()
        if not preserve:
            pairs = []
            idx = 0
            for k, v in _copy.d.items():

                pairs.append((k, v))
                idx += 1
            pairs.reverse()
            _copy.d = OrderedDict(pairs)
        else:
            _items.reverse()
            _copy.d = OrderedDict(_items)
        return _copy


class RDictEntry(ExtRegistryEntry):
    _about_ = RDict

    def compute_result_annotation(self, s_value_cls):
        assert isinstance(s_value_cls, annmodel.SomePBC)
        clsdef = self.bookkeeper.getuniqueclassdef(s_value_cls.const)
        return SomeRDict(clsdef)

    def specialize_call(self, hop):
        return hop.r_result.rtyper_new(hop)


class SomeRDict(annmodel.SomeObject):
    def __init__(self, clsdef):
        self.clsdef = clsdef

    def rtyper_makerepr(self, rtyper):
        instance_repr = rtyper.makerepr(annmodel.SomeInstance(self.clsdef))
        return RDictRepr(rtyper, instance_repr)

    def rtyper_makekey(self):
        return (self.__class__, self.clsdef)

    def method_copy(self):
        return SomeRDict(self.clsdef)

    def method_iter(self):
        return SomeRDictIter(self)

    def len(self):
        return annmodel.SomeInteger(nonneg=True)


class SomeRDictIter(annmodel.SomeObject):
    def __init__(self, rdict):
        self.rdict = rdict

    def method_next(self):
        return annmodel.SomeInstance(self.rdict.clsdef)

    def method_nextitem(self):
        return annmodel.SomeTuple([annmodel.SomeString(),
                                   annmodel.SomeInstance(self.rdict.clsdef)])

    def rtyper_makerepr(self, rtyper):
        return RDictIterRepr(rtyper, rtyper.makerepr(self.rdict))

    def rtyper_makekey(self):
        return (self.__class__, self.rdict.rtyper_makekey())


class __extend__(pairtype(SomeRDict, annmodel.SomeString)):
    def getitem((self, s_item)):
        return annmodel.SomeInstance(self.clsdef)

    def setitem((self, s_item), s_value):
        assert s_value.classdef.issubclass(self.clsdef)
        return annmodel.s_None

    def contains((self, s_item)):
        return annmodel.SomeBool()


class __extend__(pairtype(SomeRDict, annmodel.SomeInteger)):
    def getitem((self, s_item)):
        return annmodel.SomeInstance(self.clsdef)

    def setitem((self, s_item), s_value):
        assert s_value.classdef.issubclass(self.clsdef)
        return annmodel.s_None

    def contains((self, s_item)):
        return annmodel.SomeBool()


class __extend__(pairtype(SomeRDict, SomeRDict)):
    def union((self, other)):
        assert self.clsdef == other.clsdef


def new_dict_lltype(instance_lltype):
    DICTENTRY = lltype.Struct('RDICTENTRY',
                              ('key', lltype.Ptr(STR)),
                              ('value', instance_lltype),
                              ('next', lltype.Signed))

    entrymeths = {
        'valid': lldict.ll_valid,
    }
    fields = [('num_items', lltype.Signed),
              ('resize_counter', lltype.Signed),
              ('first_entry', lltype.Signed),
              ('last_entry', lltype.Signed),
              ('entries', lltype.Ptr(lltype.GcArray(DICTENTRY,
                                                    adtmeths=entrymeths)))]
    return lltype.Ptr(lltype.GcStruct('RDICT', *fields))


class RDictRepr(Repr):
    def __init__(self, rtyper, instance_repr):
        self.rtyper = rtyper
        self.instance_repr = instance_repr
        self.str_repr = rtyper.makerepr(annmodel.SomeString())
        self.lowleveltype = new_dict_lltype(instance_repr.lowleveltype)

    def rtyper_new(self, hop):
        hop.exception_cannot_occur()
        c_TP = hop.inputconst(lltype.Void, self.lowleveltype.TO)
        return hop.gendirectcall(lldict.ll_newdict, c_TP)

    def rtype_method_copy(self, hop):
        hop.exception_cannot_occur()
        v_self, = hop.inputargs(self)
        return hop.gendirectcall(lldict.ll_copy, v_self)

    def rtype_method_iter(self, hop):
        hop.exception_cannot_occur()
        v_self, = hop.inputargs(self)
        TP = hop.r_result.lowleveltype.TO
        c_TP = hop.inputconst(lltype.Void, TP)
        return hop.gendirectcall(lldict.ll_new_iter, c_TP, v_self)

    def rtype_len(self, hop):
        hop.exception_cannot_occur()
        v_self, = hop.inputargs(self)
        return hop.gendirectcall(lldict.ll_len, v_self)


class __extend__(pairtype(RDictRepr, StringRepr)):
    def rtype_getitem((self, r_item), hop):
        [v_self, v_item] = hop.inputargs(self, self.str_repr)
        hop.has_implicit_exception(KeyError)
        hop.exception_is_here()
        return hop.gendirectcall(lldict.ll_getitem_str, v_self, v_item)

    def rtype_setitem((self, r_item), hop):
        [v_self, v_item, v_value] = hop.inputargs(self, self.str_repr,
                                                  self.instance_repr)
        hop.exception_cannot_occur()
        return hop.gendirectcall(lldict.ll_setitem_str, v_self, v_item,
                                 v_value)

    def rtype_contains((self, r_item), hop):
        [v_self, v_item] = hop.inputargs(self, self.str_repr)
        hop.exception_cannot_occur()
        return hop.gendirectcall(lldict.ll_contains_str, v_self, v_item)


class __extend__(pairtype(RDictRepr, IntegerRepr)):
    def rtype_getitem((self, r_item), hop):
        xxx

    def rtype_setitem((self, r_item), hop):
        [v_self, v_item, v_value] = hop.inputargs(self, r_item,
                                                  self.instance_repr)
        hop.exception_cannot_occur()
        return hop.gendirectcall(lldict.ll_setitem_int, v_self, v_item,
                                 v_value)

    def rtype_contains((self, r_item), hop):
        xxx


class RDictIterRepr(Repr):
    def __init__(self, rtyper, parent_repr):
        self.lowleveltype = lltype.Ptr(
            lltype.GcStruct('RDICTITER',
                            ('curkey', lltype.Signed),
                            ('rdict', parent_repr.lowleveltype)))

    def rtype_method_next(self, hop):
        [v_self] = hop.inputargs(self)
        hop.exception_is_here()
        return hop.gendirectcall(lldict.ll_next_iter_value, v_self)

    def rtype_method_nextitem(self, hop):
        [v_self] = hop.inputargs(self)
        hop.exception_is_here()
        c_TUPLE = hop.inputconst(lltype.Void, hop.r_result.lowleveltype.TO)
        return hop.gendirectcall(lldict.ll_next_iter_item, v_self, c_TUPLE)
