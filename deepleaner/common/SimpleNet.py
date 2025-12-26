## 定一个一个简单神经网络

import numpy as np
from sympy.physics.vector import gradient

from deepleaner.common.function import softmax
from deepleaner.common.loss_function import cross_entropy_error


class SimpleNet:

    def __init__(self):
        self.W = np.random.randn(2, 3)
        # 前向传播
        self.b = np.zeros(3)

    def forward(self, x):
        a = x @ self.W + self.b
        # 激活函数
        y = softmax(a)
        return y

    ## 损失函数
    def loss(self, x, t):
        y = self.forward(x)
        return cross_entropy_error(y, t)

    def gradient(self, f: callable, x):
        """
        梯度计算
        """
        h = 1e-4
        gradient = np.zeros_like(x)

        for i in range(len(x)):
            a = x[i]
            x[i] = a + h
            fxh1 = f(x)
            x[i] = a - h
            fxh2 = f(x)
            x[i] = a
            gradient[i] = (fxh1 - fxh2) / (2 * h)

        return np.array(gradient)


if __name__ == "__main__":
    net = SimpleNet()
    x = np.array([0.6, 0.9])
    t = np.array([0, 0, 1])

    f = lambda x: net.loss(x, t)
    gradient = net.gradient(f, x)

    print("梯度:", gradient)
    ## 计算梯度
