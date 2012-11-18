""" Util module for compiling """

HEX_CHARS = list('01234567890ABCDEFabcdef')
OCT_CHARS = list('01234567')

double_quoted_replace_chars = {
    'n': '\n',
    'r': '\r',
    't': '\t',
    'v': '\v',
    'e': '\x1b',
    'f': '\f',
    '\\': '\\',
    '$': '$',
    '"': '"',
}


def process_single_quoted_string(string):
    last_end = 0
    result = []

    index = string.find('\\', last_end)
    while index >= 0:
        if index > last_end:
            result.append(string[last_end:index])

        next_char = string[index + 1]
        if next_char in ['\'', '\\']:
            result.append(next_char)
            last_end = index + 2
        else:
            result.append('\\')
            last_end = index + 1

        index = string.find('\\', last_end)

    result.append(string[last_end:])

    return "".join(result)


def process_double_quoted_string(string):
    last_end = 0
    string_len = len(string)
    result = []

    index = string.find('\\', last_end)
    while index >= 0:
        if index > last_end:
            result.append(string[last_end:index])

        next_char = string[index + 1]
        if next_char in double_quoted_replace_chars:
            char = double_quoted_replace_chars[next_char]
            result.append(char)
            last_end = index + 2

        elif next_char in ['x', 'X']:  # matching chars in HEX format
            matched_symbols = []
            offset = index + 2
            while offset < index + 4 and offset < string_len:
                next_char = string[offset]
                if next_char in HEX_CHARS:
                    matched_symbols.append(next_char)
                    offset += 1
                    continue

                break

            if matched_symbols:
                char = chr(int("".join(matched_symbols), 16))
                result.append(char)
                last_end = index + 2 + len(matched_symbols)
            else:
                result.append('\\')
                last_end = index + 1

        elif next_char in OCT_CHARS:  # matching chars in OCT format
            matched_digits = [next_char]
            offset = index + 2
            while offset < index + 4 and offset < string_len:
                next_char = string[offset]
                if next_char in OCT_CHARS:
                    matched_digits.append(next_char)
                    offset += 1
                    continue

                break

            char = chr(int("".join(matched_digits), 8))
            result.append(char)
            last_end = index + 1 + len(matched_digits)

        else:
            result.append('\\')
            last_end = index + 1

        index = string.find('\\', last_end)

    result.append(string[last_end:])

    return "".join(result)
