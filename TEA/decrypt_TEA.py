from ctypes import c_uint32
def decrypt(v, k):
    v0 = c_uint32(v[0])
    v1 = c_uint32(v[1])
    # delta输入题目对应的
    delta = 195935983
    # TEA解密的初始sum值是加密轮数(32) * delta
    sum1 = c_uint32(delta * 32)
    # 进行32轮解密
    for i in range(32):
        # 逆序执行加密的第二步
        v1.value -= (((v0.value << 4) ^ (v0.value >> 7)) + v0.value) ^ (sum1.value + k[(sum1.value >> 9) & 3])
        # 逆序执行加密的sum更新
        sum1.value -= delta
        # 逆序执行加密的第一步
        v0.value -= (((v1.value << 4) ^ (v1.value >> 7)) + v1.value) ^ (sum1.value + k[sum1.value & 3])
    return (v0.value, v1.value)

if __name__ == '__main__':
    # 加密密钥 (k)，输入
    k = [255, 187, 51, 68]
    # 加密后数据
    enc = [
        0xEEC7D402,
        0x99E9363F,
        0x853BDE61,
        558171287,
        0x908F94B0,
        1715140098,
        986348143,
        1948615354
    ]
    # 存储解密后的结果
    decrypted_values = []
    # 每次处理两个32位整数（即8个ASCII字符）
    for i in range(0, len(enc), 2):
        v1_enc = enc[i]
        v2_enc = enc[i+1]
        # 调用解密函数
        v1_dec, v2_dec = decrypt([v1_enc, v2_enc], k)
        # 将解密得到的32位整数转换回4个字节
        decrypted_values.append(v1_dec)
        decrypted_values.append(v2_dec)
    # 将所有解密后的32位整数组合起来，并转换为最终的flag字符串
    flag_bytes = b"" #b"" 是 Python 中表示 字节串（bytes） 的语法。
    for val in decrypted_values:
        flag_bytes += val.to_bytes(4, byteorder='big') #.to_bytes(length, byteorder, ...) 方法，这是 Python 中 整数对象（int）的一个方法，用于将整数转换为指定长度的字节串。
        
    # 尝试将字节串解码为ASCII字符串
    try:
        flag_str = flag_bytes.decode('ascii')
        print(f"这是flag: flag{{{flag_str}}}")
    except UnicodeDecodeError:
        print("Error: Decrypted bytes could not be decoded to ASCII string.")
        print(f"Raw decrypted bytes: {flag_bytes}")
