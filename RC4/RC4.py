def rc4_init(key: bytes):
    """ RC4 的 KSA 算法：根据 key 初始化 S 盒 """
    S = list(range(256))  # 初始化 S 为 0-255
    j = 0
    key_len = len(key)
    for i in range(256):
        j = (j + S[i] + key[i % key_len]) & 0xFF  # &0xFF 保证字节范围
        S[i], S[j] = S[j], S[i]  # 交换 S[i] 和 S[j]
    return S


def rc4_generate_keystream(S, length: int):
    """ RC4 的 PRGA 算法：基于初始化的 S 产生 length 个密钥流字节 """
    i = 0
    j = 0
    keystream = []
    for _ in range(length):
        i = (i + 1) & 0xFF
        j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) & 0xFF]
        keystream.append(K)
    return keystream


def rc4_encrypt(key: bytes, plaintext: bytes) -> bytes:
    """ 用 RC4 对 plaintext 加密（也可解密） """
    S = rc4_init(key)  # KSA 初始化 S
    keystream = rc4_generate_keystream(S, len(plaintext))  # PRGA 生成密钥流
    ciphertext = bytes([p ^ k for p, k in zip(plaintext, keystream)])  # 明文与密钥流异或
    return ciphertext


# 测试
if __name__ == "__main__":
    key = b"12345678abcdefghijklmnopqrspxyz"
    plaintext = b"Hello, RC4 encryption!"
    cipher = rc4_encrypt(key, plaintext)
    print("密文:", cipher.hex())

    # 解密用同样函数，异或密文和密钥流
    decrypted = rc4_encrypt(key, cipher)
    print("解密:", decrypted.decode())
