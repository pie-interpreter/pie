""" Util module for compiling """

HEX_CHARS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f']
OCT_CHARS = ['0', '1', '2', '3', '4', '5', '6', '7']

def validate_oct(string):
    index = 0
    string_len = len(string)
    result = []

    while index < string_len:
        char = string[index]
        if char not in OCT_CHARS:
            return "".join(result)

        result.append(char)
        index += 1

    return "".join(result)

def process_single_quoted_string(string):
    index = 0
    string_len = len(string)
    result = []

    while index < string_len:
        char = string[index]
        if char == '\\':
            next_char = string[index + 1]
            if next_char == '\'' or next_char == '\\':
                char = next_char
                index += 1

        result.append(char)
        index += 1

    return "".join(result)

def process_double_quoted_string(string):
    index = 0
    string_len = len(string)
    replace_chars = {
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
    result = []

    while index < string_len:
        char = string[index]
        if char == '\\':
            next_char = string[index + 1]
            if next_char in replace_chars:
                char = replace_chars[next_char]
                index += 1
            elif next_char == 'x' or next_char == 'X':
                matched_digits = []
                offset = index + 2
                while offset < index + 4 and offset < string_len:
                    next_char = string[offset]
                    if next_char in HEX_CHARS:
                        matched_digits.append(next_char)
                        offset += 1
                    else:
                        matched_digits = []
                        break

                if matched_digits:
                    index += len(matched_digits) + 1
                    char = chr(int("".join(matched_digits), 16))

            else:
                matched_digits = []
                offset = index + 2
                while offset < index + 5 and offset < string_len:
                    next_char = string[offset]
                    if next_char in OCT_CHARS:
                        matched_digits.append(next_char)
                        offset += 1
                    else:
                        matched_digits = []
                        break

                if matched_digits:
                    index += len(matched_digits)
                    char = chr(int("".join(matched_digits[1:]), 16))


        result.append(char)
        index += 1

    return "".join(result)
