
from rpython.rtyper.lltypesystem import lltype, rclass
from rpython.rtyper.annlowlevel import hlstr
from rpython.rlib.rarithmetic import intmask,  LONG_BIT, r_uint
from rpython.rlib import jit
from rpython.rlib.objectmodel import specialize

HIGHEST_BIT = intmask(1 << (LONG_BIT - 1))
MASK = intmask(HIGHEST_BIT - 1)
DICT_INITSIZE = 8
PERTURB_SHIFT = 5

@jit.elidable
def hash_string(s):
    if not s:
        return 0
    x = s.hash
    if x == 0:
        x = _hash_string(s.chars)
        if x == 0:
            x = 29872897
        s.hash = x
    return x

def _hash_string(s):
    length = len(s)
    if length == 0:
        return -1
    x = ord(s[0]) << 7
    i = 0
    while i < length:
        x = intmask((1000003*x) ^ ord(s[i]))
        i += 1
    x ^= length
    return intmask(x)

@specialize.arg(3)
@jit.look_inside_iff(lambda d, key, hash, eq: jit.isvirtual(d) and jit.isconstant(key))
def ll_dict_lookup(d, key, hash, eqfn):
    entries = d.entries
    mask = len(entries) - 1
    i = hash & mask
    # do the first try before any looping
    if entries.valid(i):
        checkingkey = entries[i].key
        if checkingkey.hash == hash:
            # correct hash, maybe the key is e.g. a different pointer to
            # an equal object
            found = eqfn(checkingkey, key)
            if found:
                return i   # found the entry
    else:
        return i | HIGHEST_BIT # pristine entry -- lookup failed

    # In the loop, a deleted entry (everused and not valid) is by far
    # (factor of 100s) the least likely outcome, so test for that last.
    entries = d.entries
    mask = len(entries) - 1
    freeslot = -1
    perturb = r_uint(hash)
    while 1:
        # compute the next index using unsigned arithmetic
        i = r_uint(i)
        i = (i << 2) + i + perturb + 1
        i = intmask(i) & mask
        # keep 'i' as a signed number here, to consistently pass signed
        # arguments to the small helper methods.
        if not entries.valid(i):
            if freeslot == -1:
                freeslot = i
            return freeslot | HIGHEST_BIT
        else:
            checkingkey = entries[i].key
            if entries[i].key.hash == hash:
                # correct hash, maybe the key is e.g. a different pointer to
                # an equal object
                found = eqfn(checkingkey, key)
                if found:
                    return i   # found the entry
        perturb >>= PERTURB_SHIFT

def eq_str(ll_s1, ll_s2):
    if ll_s1 == ll_s2:
        return True
    return hlstr(ll_s1) == hlstr(ll_s2)

def ll_valid(entries, i):
    return bool(entries[i].key)

def ll_get_value(d, i):
    return d.entries[i].value

def ll_getitem_str(dct, ll_s):
    i = ll_dict_lookup(dct, ll_s, hash_string(ll_s), eq_str)
    if not i & HIGHEST_BIT:
        return ll_get_value(dct, i)
    else:
        raise KeyError

def ll_contains_str(dct, ll_s):
    i = ll_dict_lookup(dct, ll_s, hash_string(ll_s), eq_str)
    if not i & HIGHEST_BIT:
        return True
    else:
        return False

def ll_setitem_str(dct, ll_s, ll_v):
    hash = hash_string(ll_s)
    i = ll_dict_lookup(dct, ll_s, hash, eq_str)
    return _ll_dict_setitem_lookup_done(dct, ll_s, ll_v, hash, i)

@jit.look_inside_iff(lambda d, key, value, hash, i: jit.isvirtual(d) and jit.isconstant(key))
def _ll_dict_setitem_lookup_done(d, key, value, hash, i):
    valid = (i & HIGHEST_BIT) == 0
    i = i & MASK
    everused = d.entries.valid(i)
    # set up the new entry
    entry = d.entries[i]
    entry.value = value
    if valid:
        return
    entry.key = key
    d.num_items += 1
    if not everused:
        d.resize_counter -= 3
        if d.first_entry == -1:
            d.first_entry = i
        else:
            d.entries[d.last_entry].next = i
        d.last_entry = i
        if d.resize_counter <= 0:
            ll_dict_resize(d)
    # otherwise we don't touch the order

def ll_dict_resize(d):
    old_entries = d.entries
    old_size = len(old_entries)
    # make a 'new_size' estimate and shrink it if there are many
    # deleted entry markers
    new_size = old_size * 2
    DICT = lltype.typeOf(d)
    d.entries = lltype.malloc(DICT.TO.entries.TO, new_size, zero=True)
    d.num_items = 0
    d.resize_counter = new_size * 2
    i = d.first_entry
    hash = old_entries[i].key.hash
    entry = old_entries[i]
    prev_index = ll_dict_insertclean(d, entry.key, entry.value, hash,
                                     -1)
    d.first_entry = prev_index
    i = entry.next
    while i != d.last_entry:
        hash = old_entries[i].key.hash
        entry = old_entries[i]
        prev_index = ll_dict_insertclean(d, entry.key, entry.value, hash,
                                         prev_index)
        i = entry.next
    hash = old_entries[i].key.hash
    entry = old_entries[i]
    prev_index = ll_dict_insertclean(d, entry.key, entry.value, hash,
                                     prev_index)
    i = entry.next
    d.last_entry = prev_index

def ll_dict_insertclean(d, key, value, hash, prev_index):
    # Internal routine used by ll_dict_resize() to insert an item which is
    # known to be absent from the dict.  This routine also assumes that
    # the dict contains no deleted entries.  This routine has the advantage
    # of never calling d.keyhash() and d.keyeq(), so it cannot call back
    # to user code.  ll_dict_insertclean() doesn't resize the dict, either.
    i = ll_dict_lookup_clean(d, hash)
    entry = d.entries[i]
    entry.value = value
    entry.key = key
    if prev_index != -1:
        d.entries[prev_index].next = i
    d.num_items += 1
    d.resize_counter -= 3
    return i

def ll_dict_lookup_clean(d, hash):
    # a simplified version of ll_dict_lookup() which assumes that the
    # key is new, and the dictionary doesn't contain deleted entries.
    # It only finds the next free slot for the given hash.
    entries = d.entries
    mask = len(entries) - 1
    i = hash & mask
    perturb = r_uint(hash)
    while entries.valid(i):
        i = r_uint(i)
        i = (i << 2) + i + perturb + 1
        i = intmask(i) & mask
        perturb >>= PERTURB_SHIFT
    return i

def ll_len(d):
    return d.num_items

def ll_newdict(DICT):
    d = lltype.malloc(DICT)
    d.entries = lltype.malloc(DICT.entries.TO, DICT_INITSIZE, zero=True)
    d.num_items = 0
    d.first_entry = -1
    d.last_entry = -1
    d.resize_counter = DICT_INITSIZE * 2
    return d

def ll_copy(dct):
    DICT = lltype.typeOf(dct).TO
    dictsize = len(dct.entries)
    d = lltype.malloc(DICT)
    d.entries = lltype.malloc(DICT.entries.TO, dictsize, zero=True)
    d.num_items = dct.num_items
    d.resize_counter = dct.resize_counter
    d.first_entry = dct.first_entry
    d.last_entry = dct.last_entry
    i = 0
    while i < dictsize:
        d_entry = d.entries[i]
        entry = dct.entries[i]
        d_entry.key = entry.key
        d_entry.value = entry.value
        i += 1
    return d

def ll_new_iter(TP, dct):
    dictiter = lltype.malloc(TP)
    dictiter.rdict = dct
    dictiter.curkey = dct.first_entry
    return dictiter

def ll_next_iter_value(dictiter):
    if dictiter.rdict.first_entry == -1:
        # empty dict
        raise StopIteration
    entries = dictiter.rdict.entries
    curkey = dictiter.curkey
    if curkey == -1:
        raise StopIteration
    res = entries[curkey].value
    if curkey == dictiter.rdict.last_entry:
        dictiter.curkey = -1
    else:
        dictiter.curkey = entries[curkey].next
    return res

def ll_next_iter_item(dictiter, TP):
    if dictiter.rdict.first_entry == -1:
        # empty dict
        raise StopIteration
    entries = dictiter.rdict.entries
    curkey = dictiter.curkey
    if curkey == -1:
        raise StopIteration
    key = entries[curkey].key
    value = entries[curkey].value
    if curkey == dictiter.rdict.last_entry:
        dictiter.curkey = -1
    else:
        dictiter.curkey = entries[curkey].next
    res = lltype.malloc(TP)
    res.item0 = key
    res.item1 = lltype.cast_pointer(rclass.OBJECTPTR, value)
    return res
