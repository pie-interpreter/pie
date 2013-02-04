from rpython.rlib.parsing.parsing import ParseError

__author__ = "sery0ga"


def raw_parse_ini_file(filename, process_sections=False, scanner_mode=0):
    fp = open(filename)
    result = _read_file(fp)
    fp.close()
    return result


def _read_file(fp):
    """Parse a sectioned setup file.

    The sections in setup file contains a title line at the top,
    indicated by a name in square brackets (`[]'), plus key/value
    options lines, indicated by `name: value' format lines.
    Continuations are represented by an embedded newline then
    leading whitespace.  Blank lines, lines beginning with a '#',
    and just about everything else are ignored.
    """
    cursect = None                        # None, or a dictionary
    sections = {}
    lineno = 0
    while True:
        line = fp.readline()
        if not line:
            break
        lineno = lineno + 1
        # comment or blank line?
        line = line.strip()
        if line == '' or line[0] in '#;':
            #TODO: show DEPRECATED error on #
            continue
        length = len(line)
        if line[0] == '[':
            if line[length - 1] != ']':
                # this is a parsing error
                # Don't care about warnings - do it later with normal parsing
                raise ParseError("Section should have a closing bracket", lineno)
            # handle section
            cursect = line[1:length - 1].strip()
            if cursect not in sections:
                sections[cursect] = {}
        else:
            # handle option line
            begin = 0
            name = ''
            value = ''
            string = False
            (NAME, VALUE) = range(2)
            state = NAME
            for index in range(length):
                if line[index] == '=' and state == NAME:
                    name = line[0:index - 1].strip()
                    begin = index + 1
                    state = VALUE
                elif state == VALUE and line[index] == '"':
                    if not string:
                        string = True
                        begin = index + 1
                    else:
                        if begin < index:
                            value = line[begin:index]
                            break
            if not name:
                # this is a parsing error
                # Don't care about warnings - do it later with normal parsing
                raise ParseError("Each option should have name and value", lineno)
            if value:
                sections[cursect][name] = value
            else:
                if string:  # this is a parsing error
                    raise ParseError("String should have a closing bracket", lineno)
                if begin < length:
                    sections[cursect][name] = line[begin:length].strip()

    return sections

