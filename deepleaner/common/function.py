# 阶跃函数
def step_function(x):
    if x < 0:
        return 0
    else:
        return 1


import numpy as np


def step_function(x):
    """
    这段代码 np.array(x > 0, dtype=int) 的含义如下：
x > 0：这是一个布尔运算，会对数组 x 中的每个元素进行判断，如果元素大于 0，则对应位置返回 True，否则返回 False。
这会生成一个与 x 形状相同的布尔型数组。
np.array(..., dtype=int)：将上述布尔型数组转换为整型数组。在 NumPy 中，True 会被转换为 1，False 会被转换为 0。
因此，这行代码的作用是将输入数组 x 中大于 0 的元素标记为 1，小于等于 0 的元素标记为 0，从而实现阶跃函数的功能。
    """
    return np.array(x > 0, dtype=int)


def sigmoid(x):
    """
            np.exp(-x)：计算 e 的 -x 次方，其中 e 是自然常数（约等于2.71828）。这里对数组 x 中的每个元素都进行指数运算
                1+np.exp(-x)：将上述指数结果加1
                1/(1+np.exp(-x))：计算上述结果的倒数
                Sigmoid函数的特点：
                将任意实数映射到 (0,1) 区间内
                常用于神经网络中的激活函数
                当 x 趋近于正无穷时，函数值趋近于1
                当 x 趋近于负无穷时，函数值趋近于0
                在 x=0 处，函数值为0.5
                这个函数在机器学习中非常常用，特别是在二分类问题中作为输出层的激活函数。


    """
    return 1 / (1 + np.exp(-x))


def softmax(x):
    """

    np.exp() 函数是 e^x   指数函数
    """
    x = np.array(x)
    x = x - np.max(x)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x)


## 恒等函数
def identity_function(x):
    return x


if __name__ == "__main__":
    x = np.array([0, 1, 2, 3, 4, 5, -1, - 2, -3, - 4, -5])
    y = softmax(x)
    print(y)
