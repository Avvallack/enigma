import re

BASIC_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

ROTOR_DICT = {
    1: ('AELTPHQXRU', 'BKNW', 'CMOY', 'DFG', 'IV', 'JZ', 'S'),
    2: ('FIXVYOMW', 'CDKLHUP', 'ESZ', 'BJ', 'GR', 'NT', 'A', 'Q'),
    3: ('ABDHPEJT', 'CFLVMZOYQIRWUKXSG', 'N'),
    4: ('AEPLIYWCOXMRFZBSTGJQNH', 'DV', 'KU'),
    5: ('AVOLDRWFIUQ', 'BZKSMNHYC', 'EGTJPX'),
    6: ('AJQDVLEOZWIYTS', 'CGMNHFUX', 'BPRK'),
    7: ('ANOUPFRIMBZTLWKSVEGCJYDHXQ'),
    8: ('AFLSETWUNDHOZVICQ', 'BKJ', 'GXY', 'MPR'),
    'beta': ('ALBEVFCYODJWUGNMQTZSKPR', 'HIX'),
    'gamma': ('AFNIRLBSQWVXGUZDKMTPCOYJHE'),
}

REFLECTORS = {
    1: ('AY', 'BR', 'CU', 'DH', 'EQ', 'FS', 'GL', 'IP', 'JX', 'KN', 'MO', 'TZ', 'VW'),
    2: ('AF', 'BV', 'CP', 'DJ', 'EI', 'GO', 'HY', 'KR', 'LZ', 'MX', 'NW', 'TQ', 'SU'),
    3: ('AE', 'BN', 'CK', 'DQ', 'FU', 'GY', 'HW', 'IJ', 'LO', 'MP', 'RX', 'SZ', 'TV'),
    4: ('AR', 'BD', 'CO', 'EJ', 'FN', 'GT', 'HK', 'IV', 'LM', 'PW', 'QZ', 'SX', 'UY')
}

SHIFT_PLACE = {
    1: [17],
    2: [5],
    3: [22],
    4: [10],
    5: [0],
    6: [0, 13],
    7: [0, 13],
    8: [0, 13]
}

PATTERN = re.compile('[^\w]')


def rotor(symbol, n, reverse=False):
    """
    implement the basic logic for rotor of machine
    :param symbol: char from ALPHABET
    :param n: number of rotor
    :param reverse: if router going reverse
    :return: ciphered char
    """
    if n == 0:
        return symbol
    for pattern in ROTOR_DICT[n]:
        if symbol.upper() in pattern:
            if reverse:
                return pattern[pattern.index(symbol) - 1]
            if pattern.index(symbol) + 1 < len(pattern):
                return pattern[pattern.index(symbol) + 1]
            return pattern[0]


def reflector(symbol, n):
    """
    implements basic reflector of enigma machine
    :param symbol: char
    :param n: number of reflector
    :return: reflected char
    """
    if n == 0:
        return symbol
    for elem in REFLECTORS[n]:
        if symbol.upper() in elem:
            if elem.index(symbol) == 0:
                return elem[1]
            return elem[0]


def shift(symbol, step, alphabet=BASIC_ALPHABET):
    """
    implements shift of rotors logic
    :param symbol: char
    :param step: int step for shifting
    :param alphabet: optional using alphabet. Default to english uppercase
    :return: shifted character
    """
    if alphabet.index(symbol) + step < len(alphabet):
        return alphabet[alphabet.index(symbol) + step]
    return alphabet[alphabet.index(symbol) + step - len(alphabet)]


def check_position(rot, current_shift):
    if current_shift in SHIFT_PLACE[rot]:
        return True
    return False


def cut_shift(current_shift):
    if current_shift >= len(BASIC_ALPHABET):
        return current_shift % len(BASIC_ALPHABET)
    return current_shift


def commutation(letters):
    if letters:
        let_array = letters.upper().split()
        if len(''.join(let_array)) == len(set(''.join(let_array))):
            return let_array
        else:
            return -1


def replace_char(char, current_commutation):
    if current_commutation:
        for item in current_commutation:
            if char in item:
                char = item[0] if item.index(char) == 1 else item[1]
                return char
    return char


def enigma(text, ref, rot1, shift1, rot2, shift2, rot3, shift3, pairs=''):
    """
    implementation of enigma machine working with three rotors
    :param text: text to cipher
    :param ref: reflector key from REFLECTOR_DICT
    :param rot1: rotor1 key from ROTOR_DICT
    :param shift1: starting shift for rotor 1
    :param rot2: rotor2 key from ROTOR_DICT
    :param shift2: starting shift for rotor 2
    :param rot3: rotor3 key from ROTOR_DICT
    :param shift3: starting shift for rotor 3
    :param pairs: pairs of letters for commutation expected to be pairs of letters splitted by space f.e. 'AB XD'
    :return: ciphered text
    """
    current_commutation = commutation(pairs)
    if current_commutation == -1:
        return 'Inapplicable commutation'
    output = ''
    text = re.sub(PATTERN, '', text.upper())
    for char in text:
        if check_position(rot2, shift2 + 1):
            shift2 += 1
            shift2 = cut_shift(shift2)
            shift1 += 1
            shift1 = cut_shift(shift1)

        shift3 += 1
        shift3 = cut_shift(shift3)

        if check_position(rot3, shift3):
            shift2 += 1
            shift2 = cut_shift(shift2)

        char = replace_char(char, current_commutation)

        char = shift(char, shift3)
        char = rotor(char, rot3)
        char = shift(char, shift2 - shift3)
        char = rotor(char, rot2)
        char = shift(char, shift1 - shift2)
        char = rotor(char, rot1)
        char = shift(char, -shift1)
        char = reflector(char, ref)
        char = shift(char, shift1)
        char = rotor(char, rot1, reverse=True)
        char = shift(char, shift2 - shift1)
        char = rotor(char, rot2, reverse=True)
        char = shift(char, shift3 - shift2)
        char = rotor(char, rot3, reverse=True)
        char = shift(char, -shift3)
        char = replace_char(char, current_commutation)

        output += char

    return output
