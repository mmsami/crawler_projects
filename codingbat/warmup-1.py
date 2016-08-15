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


if __name__ == '__main__':
    print diff21(23)
    print pos_neg(-4, -5, True)
