"""
duermevela utility functions.
"""


def cgtime2secs(cgtime):
    """ calculate the number of seconds in an "m'ss" time string, ie: "1'07" -> 67. """

    m, s = cgtime.split("'")
    return int(m) * 60 + int(s)


def secs2cgtime(secs):
    """ format seconds into "m'ss" clock format, ie: 67 -> "1'07". """

    secs = int(secs)
    return f"{'' if secs > 0 else '-'}{abs(secs) // 60:d}'{abs(secs) % 60:02d}"
