"""
duermevela utility functions.
"""


def cage_time(s):
    """ format seconds into "m'ss" clock format, ie: 67 -> "1'07". """

    s = int(s)
    return f"{s // 60:d}'{s % 60:02d}"
