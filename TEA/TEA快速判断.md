# TEA快速判断

| 观察数据类型 | `c_uint32`、`bytes_to_long` → 说明是按 32 位整数处理，常见于 TEA、XTEA、RC5 等 |
| ------------ | ------------------------------------------------------------ |
| 看循环次数   | `range(32)` → XTEA 标准是 32 轮（64 轮是 XXTEA）             |
| 看轮函数结构 | `(v1<<4 ^ v1>>7) + v1 ^ sum + k[...]` → 典型 TEA 混淆函数    |

# **加密函数说明**

**`Crypto.Util.number` 是 `pycryptodome` 库的一部分。**

```bash
pip install pycryptodome //安装pycryptodome
```

整体流程概览：

1. 用户输入一个 flag。
2. 检查 flag 长度是否为 32 字符。
3. 将 flag 分成 4 组，每组 8 字符，再每 4 字符转为一个 32 位整数（共 8 个整数）。
4. 使用自定义的 `encrypt()` 函数对每组两个整数进行加密（使用 TEA 变种算法）。
5. 加密结果与预设的 `enc` 数组比较，若完全一致，则 flag 正确。

# 解密脚本编写

第一部分，是TEA类型解密。这里给出我总结的模板。

也就是说，TEA或其变种的解密，需要关注的就是delta和sum值，而解密的初始sum1值是加密轮数(32) * delta这个逻辑是固定的，逆序解密步骤是从加密的第二步倒退回去。

```python
from ctypes import c_uint32
def decrypt(v, k):
    v0 = c_uint32(v[0])
    v1 = c_uint32(v[1])
    # delta输入题目对应的
    delta = 
    # TEA解密的初始sum1值是加密轮数(32) * delta
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
```

第二部分是enc的匹配

现在，我们整理一下思路。我们输入一个32字符长度的flag，最终会被程序拆解为总共8个长度32位的整数，然后这8个整数经过加密后，和enc中的8个整数依次匹配，全部正确就是输入了正确的flag。

也就是说，我们已知了加密后的8个整数，要倒推回原始的8个整数，然后变为原始的flag值



