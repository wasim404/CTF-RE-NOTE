# 【逆向】base64编码识别

## 特征

1. `0x3F`的掩码
2. IDA逆向字串中包含长度128/64的`a-z A-Z`的表
3. `<<6`

## 程序分析

这道题要求输入flag，说明大概率是字符串匹配，我们输入正确的字符串就是flag。因此我们必须要分析函数逻辑而不能通过修改寄存器绕过。（静态调试）

先分析结果输出判断（遇到strcmp大概率是两个字符串相等），但还是分析一下，若要输出correct，则第二个if要为假，也就是`v9==0`，若v9是0，则不会进入第一个if语句，同时v12要和you_know_how_to_remove_junk_code相同。因此，要让程序返回correct，充要条件是`v12=='you_know_how_to_remove_junk_code'`

```c
v9 = strcmp(v12, "you_know_how_to_remove_junk_code");
  if ( v9 )
    v9 = v9 < 0 ? -1 : 1;
  if ( v9 )
    printf("wrong\n");
  else
    printf("correct\n");
  system("pause");
```

继续分析，提示`junk_code`说明题目中可能存在一些无关的代码（混淆），其实就是

```c
    if ( v13 >= 0x10 )
    {
      si128 = _mm_load_si128((const __m128i *)&xmmword_244F20);
      v6 = v13 - (v13 & 0xF);
      v7 = (const __m128i *)v12;
      do
      {
        v8 = _mm_loadu_si128(v7);
        v4 += 16;
        ++v7;
        v7[-1] = _mm_xor_si128(v8, si128);
      }
      while ( v4 < v6 );
    }
```

这部分，因为这部分其实是优化性能代码。

重点是

```c
for ( ; v4 < v3; ++v4 )
      v12[v4] ^= 0x25u;
```

也就是说，v12最终结果是和0x25异或得到的

继续分析前面仅剩的最关键的函数

```c
sub_231000(v11, strlen(v11));
```

进入函数内部，根据上面的特征，可以判断出这是一个base64相关函数

| 特征         | 解码                 | 编码                    |
| ------------ | -------------------- | ----------------------- |
| 输入字节数量 | 4 个字符             | 3 个字节                |
| 输出字节数量 | 1~3 个               | 4 个字符                |
| 位操作       | `<<6                 | &0x3F` 循环 4 次        |
| 查表         | ASCII → 0..63        | 0..63 → ASCII           |
| 填充符       | `'='` → 输出字节补齐 | `'='` → 输入不足 3 字节 |

> 简单口诀：
>
> - **4 字符 → 3 字节 → 解码**
> - **3 字节 → 4 字符 → 编码**

判断出这是base64解码

那么程序整体逻辑就是：输入flag---->base64解码---->异或0x25---->得到'you_know_how_to_remove_junk_code'

## 解密脚本

```py
import base64
str_input = "you_know_how_to_remove_junk_code"
xored = "".join([chr(ord(c) ^ 0x25) for c in str_input])
xored_bytes = xored.encode('latin1')  # 用 latin1 保证每个字节对应 0-255
b64_encoded = base64.b64encode(xored_bytes).decode('utf-8')
print("最终 Base64 编码：", b64_encoded)
```

