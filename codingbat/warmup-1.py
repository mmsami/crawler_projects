# coding=utf-8
def diff21(n):
    """Given an int n, return the absolute difference between n and 21,
    except return double the absolute difference if n is over 21"""
    if n <= 21:
        return 21 - n
    else:
        return (n - 21) * 2


def pos_neg(a, b, negative):
    """Given 2 int values, return True if one is negative and one is positive.
    Except if the parameter "negative" is True, then return True only if both are negative.
    pos_neg(1, -1, False) → True
    pos_neg(-1, 1, False) → True
    pos_neg(-4, -5, True) → True"""
    if negative:
        return a < 0 and b < 0
    else:
        return (a < 0 and b > 0) or (a > 0 and b < 0)


def not_string(str):
    """Given a string, return a new string where "not " has been added to the front.
    However, if the string already begins with "not", return the string unchanged."""
    if len(str) >= 3 and str[:3] == "not":
        return str
    return "not " + str


def front_back(str):
    """Given a string, return a new string where the first and last chars have been exchanged."""
    if len(str) <= 1:
        return str

    mid = str[1:len(str) - 1]  # can be written as str[1:-1]

    # last + mid + first
    return str[len(str) - 1] + mid + str[0]


if __name__ == '__main__':
    print diff21(23)
    print pos_neg(-4, -5, True)
