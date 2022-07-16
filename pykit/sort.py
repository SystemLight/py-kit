import re
import functools


def natural_key(astr):
    return [int(s) if s.isdecimal() else s for s in re.split(r'(\d+)', astr)]


def natural_cmp(a, b):
    key_a = natural_key(a)
    key_b = natural_key(b)
    if key_a > key_b:
        return 1
    if key_a < key_b:
        return -1
    if key_a == key_b:
        return 0


def tcmp(a, b):
    return natural_cmp(a["name"], b["name"])


if __name__ == '__main__':
    results = []
    sorted(results, key=functools.cmp_to_key(tcmp))
