# -*- coding: utf-8 -*-

def length(n):
    result = 0
    while n != 0:
        result += 1
        n >>= 1
    return result
