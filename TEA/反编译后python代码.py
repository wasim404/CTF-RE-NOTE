#!/usr/bin/env python
# visit https://tool.lu/pyc/ for more information
# Version: Python 3.6

from ctypes import *
from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import long_to_bytes

def encrypt(v, k):
    v0 = c_uint32(v[0])
    v1 = c_uint32(v[1])
    sum1 = c_uint32(0)
    delta = 195935983
    for i in range(32):
        v0.value += (v1.value << 4 ^ v1.value >> 7) + v1.value ^ sum1.value + k[sum1.value & 3]
        sum1.value += delta
        v1.value += (v0.value << 4 ^ v0.value >> 7) + v0.value ^ sum1.value + k[sum1.value >> 9 & 3]
    
    return (v0.value, v1.value)

if __name__ == '__main__':
    flag = input('please input your flag:')
    k = [
        255,
        187,
        51,
        68]
    if len(flag) != 32:
        print('wrong!')
        exit(-1)
    a = []
    for i in range(0, 32, 8):
        v1 = bytes_to_long(bytes(flag[i:i + 4], 'ascii'))
        v2 = bytes_to_long(bytes(flag[i + 4:i + 8], 'ascii'))
        a += encrypt([
            v1,
            v2], k)
    
    enc = [
        0xEEC7D402,
        0x99E9363F,
        0x853BDE61,
        558171287,
        0x908F94B0,
        1715140098,
        986348143,
        1948615354]
    for i in range(8):
        if enc[i] != a[i]:
            print('wrong!')
            exit(-1)
    print('flag is flag{%s}' % flag)
