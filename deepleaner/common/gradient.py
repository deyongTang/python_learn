import numpy as np


# 求导数，微分

def numerial_diff(f, x):
    h = 1e-4  # 微小值 0.0001
    # 中心差分
    return (f(x + h) - f(x - h)) / (2 * h)


def numerical_gradient(f, x):
    """数值梯度（中心差分），支持多维数组。"""
    h = 1e-4
    grad = np.zeros_like(x)
    it = np.nditer(x, flags=["multi_index"], op_flags=["readwrite"])

    while not it.finished:
        idx = it.multi_index
        tmp = x[idx]

        x[idx] = tmp + h
        fxh1 = f(x)

        x[idx] = tmp - h
        fxh2 = f(x)

        grad[idx] = (fxh1 - fxh2) / (2 * h)
        x[idx] = tmp
        it.iternext()

    return grad


if __name__ == "__main__":
    def f(x):
        return x ** 2

    print(numerial_diff(f, 5))
