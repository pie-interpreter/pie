"""
This is a part of ntpath.py standard library file. It was rewritten in RPython
style.
"""
__author__ = 'sery0ga'


# Return the tail (basename) part of a path.


def basename(path):
    """Returns the final component of a pathname"""
    return split_path(path)[1]

# Return the head (dirname) part of a path.


def dirname(path):
    """Returns the directory component of a pathname"""
    return split_path(path)[0]

# Split a path in head (everything up to the last '/') and tail (the
# rest).  After the trailing '/' is stripped, the invariant
# join(head, tail) == p holds.
# The resulting head won't end in '/' unless it is the root.


def split_path(path):
    """Split a pathname.

    Return tuple (head, tail) where tail is everything after the final slash.
    Either part may be empty."""

    length = len(path)
    index = length - 1
    while index >= 0 and path[index] not in '/\\':
        index -= 1
    if index >= 0:
        tail = path[index:length]  # now tail has no slashes
    else:
        return '', path
    # remove trailing slashes from head, unless it's all slashes
    while index >= 0 and path[index] in '/\\':
        index -= 1
    if index >= 0:
        head = path[0:index + 1]
    else:
        head = ''
    return head, tail
