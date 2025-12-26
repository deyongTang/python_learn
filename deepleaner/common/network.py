import numpy as np

try:
    from deepleaner.common.function import sigmoid, identity_function
except ImportError:  # pragma: no cover
    from function import sigmoid, identity_function


def init_network():
    # 固定参数的三层全连接网络：2 -> 3 -> 2 -> 2
    network = {}
    network['W1'] = np.array([
        [0.1, 0.3, 0.5],
        [0.2, 0.4, 0.6]
    ])

    network['b1'] = np.array([0.1, 0.2, 0.3])
    network['W2'] = np.array([
        [0.1, 0.4],
        [0.2, 0.5],
        [0.3, 0.6]
    ])
    network['b2'] = np.array([0.1, 0.2])
    network['W3'] = np.array([
        [0.1, 0.3],
        [0.2, 0.4]
    ])
    network['b3'] = np.array([0.1, 0.2])
    return network
"""
            dot 是“点积/矩阵乘法”的意思，NumPy 里常用 np.dot 来做线性代数计算。

                在这个 demo 里：
                
                x 是形状 (2,) 的向量
                W1 是形状 (2, 3) 的矩阵
                np.dot(x, W1) 的结果是形状 (3,) 的向量
                也就是把输入映射到 3 个神经元上
                公式上就是：
                
                a_j = x1 * W1[0, j] + x2 * W1[1, j]
                补充说明：
                
                向量 · 向量 → 点积（一个标量）
                向量 · 矩阵 → 向量（每列做一次点积）
                矩阵 · 矩阵 → 矩阵
                在 NumPy 里 A @ B 和 np.dot(A, B) 在二维矩阵情况下等价。

"""

## 前向传播
def forward(network, x):
    W1, W2, W3 = network['W1'], network['W2'], network['W3']
    b1, b2, b3 = network['b1'], network['b2'], network['b3']
    # 第 1 层：线性变换 + 激活
    a1 = np.dot(x, W1) + b1
    z1 = sigmoid(a1)
    # 第 2 层：线性变换 + 激活
    a2 = np.dot(z1, W2) + b2
    z2 = sigmoid(a2)
    # 输出层：线性变换 + 恒等映射
    a3 = np.dot(z2, W3) + b3

    y = identity_function(a3)
    return y


if __name__ == '__main__':
    network = init_network()
    x = np.array([1.0, 0.5])
    y = forward(network, x)
    print(y)
