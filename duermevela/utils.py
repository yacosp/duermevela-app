"""
duermevela utility functions.
"""


def cgtime2secs(cgtime):
    """ calculate the number of seconds in an "m'ss" time string, ie: "1'07" -> 67. """

    m, s = cgtime.split("'")
    return int(m) * 60 + int(s)


def secs2cgtime(secs):
    """ format seconds into "m'ss" time string, ie: 67 -> "1'07". """

    secs = int(secs)
    return f"{'' if secs > 0 else '-'}{abs(secs) // 60:d}'{abs(secs) % 60:02d}"


def note_number(note):
    """ find the piano note number for a note, ie: a0 = 1, c8 = 88. """

    numbers = {'c': -8, 'c#': -7, 'db': -7, 'd': -6, 'd#': -5, 'eb': -5, 'e': -4, 'e#': -3, 'f': -3,
               'f#': -2, 'gb': -2, 'g': -1, 'g#': 0, 'ab': 0, 'a': 1, 'a#': 2, 'bb': 2, 'b': 3, 'cb': 3}
    return numbers[note[:-1]] + int(note[-1:]) * 12


def note_freq(note):
    """ find the frequency of a note, ie: a4 = 440. """

    return 2 ** ((note_number(note) - 49)/12) * 440


def alnum_only(text, keep_spaces=False):
    """ strip all punctuation from a text, ie: "hola, mundo!" => "holamundo" """

    remove = "!(),.-/:;?" + ("" if keep_spaces else " ")
    return text.translate(str.maketrans("", "", remove))


def letter_value(letter):
    """ find the value of a letter, ie: "a" = 1, "z" = 27 (spanish!). """

    letter = letter.lower()
    spanish = {'á': 1, 'é': 5, 'í': 9, 'ó': 16, 'ú': 22, 'ü': 22, 'ñ': 15}

    if letter in spanish:
        return spanish[letter]
    elif letter in "0123456789":
        return int(letter)
    elif letter in "abcdefghijklmnopqrstuvwxyz":
        return ord(letter) - (96 if ord(letter) < ord("o") else 95)
    else:
        return 0


def letter_sum(text):
    """ return the sum of letter values in a text, ie: "lerolero" = 104. """

    return sum([letter_value(letter) for letter in alnum_only(text)])
