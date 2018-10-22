#!/usr/bin/python


gf_exp = [0] * 512
gf_log = [0] * 256


def init_tables(prim=0x11d):
    # 使用参数prim给的本原多项式计算指数表和对数表备用
    global gf_exp, gf_log
    gf_exp = [0] * 512  # anti-log (exponential指数) table
    gf_log = [0] * 256  # log(对数) table
    # 计算每一个GF(2^8)域内正整数的指数和对数
    x = 1
    for i in range(0, 255):
        gf_exp[i] = x  # 存储指数表
        gf_log[x] = i  # 存储对数表
        # 更一般的情况用下面这行，不过速度较慢
        # x = gf_mul_no_lut(x, 2, prim)
        # 只用到 generator==2 或指数底为 2的情况下，用下面的代码速度快过上面的 gf_mul_no_lut():
        x <<= 1
        if x & 0x100:  # 等效于 x >= 256, 但要更快些 (because 0x100 == 256，位运算速度优势)
            x ^= prim  # 将主多项式减为当前值(而不是255，这样我们就得到了由coprime数字组成的唯一集)，这是乘法表生成的核心

    # Optimization: 双倍指数表大小可以省去为了不出界而取模255的运算 (因为主要用这个表来计算GF域乘法，仅此而已).
    for i in range(255, 512):
        gf_exp[i] = gf_exp[i - 255]
    return [gf_log, gf_exp]


def gf_mul_no_lut(x, y, prim=0x11d, field_charac_full=256, carry_less=True):
    # 采用 Russian Peasant 算法实现GF域整数乘法 (主要使用位运算, 比上面的方法快).
    # 当设定参数prim = 0 且 carry_less=False 时, 返回普通整数乘法(进位乘法)计算结果.
    r = 0
    while y:
        if y & 1:
            r = r ^ x if carry_less else r + x
        y = y >> 1
        x = x << 1
        if prim > 0 and x & field_charac_full:
            x = x ^ prim
    return r


def gf_pow(x, _pow):
    # GF power.
    return gf_exp[(gf_log[x] * _pow) % 255]


def gf_mul(x, y):
    # Simplified GF multiplication.
    if x == 0 or y == 0:
        return 0
    return gf_exp[gf_log[x] + gf_log[y]]


def gf_poly_mul(p, q):
    # GF polynomial multiplication.
    r = [0] * (len(p) + len(q) - 1)
    for j in range(len(q)):
        for i in range(len(p)):
            r[i + j] ^= gf_mul(p[i], q[j])
    return r


def gf_poly_div(dividend, divisor):
    # 适用于GF(2^p)域的快速多项式除法.
    # 注意: 多项式系数需要按幂次由高到低排序. 例如: 1 + 2x + 5x^2 = [5, 2, 1], 而非 [1, 2, 5]
    res = list(dividend)  # 复制被除数(尾部后缀ecc字节, 用0填充)
    for i in range(len(dividend) - len(divisor) + 1):
        coef = res[i]
        if coef != 0:  # 避免log(0)未定义错误.
            for j in range(1, len(divisor)):  # 因为多项式的首位都是1, (1^1==0)所以可以跳过
                if divisor[j] != 0:
                    res[i + j] ^= gf_mul(divisor[j], coef)  # 等价于数学表达式:res[i + j] += -divisor[j] * coef ,但异或运高效
    # res 包含商和余数, 余数的最高幂次( == length-1)和除数一样, 下面计算分断点.
    sep = -(len(divisor) - 1)
    return res[:sep], res[sep:]


def rs_gen_poly(nsym):
    # Generate generator polynomial for RS algorithm.
    g = [1]
    for i in range(nsym):
        # g = gf_poly_mul(g, [1, gf_pow(2, i)]) # 指数运算，跟下面等效
        g = gf_poly_mul(g, [1, gf_exp[i]])
    return g


def rs_encode(bitstring, nsym):
    # Encode bitstring with nsym EC bits using RS algorithm.
    gen = rs_gen_poly(nsym)
    # 后缀ecc字节位用0填充, 之后用生成子(irreducible generator polynomial)除
    _, remainder = gf_poly_div(bitstring + [0] * (len(gen) - 1), gen)
    # 余数就是 RS 码! 后缀到原信息之后形成全部编码
    msg_out = bitstring + remainder
    # Return the codeword
    return msg_out
