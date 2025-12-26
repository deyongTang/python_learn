import numpy as np


def sigmoid(x):
    """Sigmoid 激活函数。"""
    return 1 / (1 + np.exp(-x))


def softmax(x):
    """Softmax：把得分转成概率（支持单样本或批量）。"""
    if x.ndim == 2:
        x = x - np.max(x, axis=1, keepdims=True)
        exp_x = np.exp(x)
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    x = x - np.max(x)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x)


def cross_entropy_error(y, t):
    """
    交叉熵损失。
    y: 预测概率，shape (batch, num_classes) 或 (num_classes,)
    t: 标签（类别索引或 one-hot）
    """
    if y.ndim == 1:
        y = y.reshape(1, -1)
        t = t.reshape(1, -1)

    # one-hot -> 索引
    if t.size == y.size:
        t = np.argmax(t, axis=1)

    batch_size = y.shape[0]
    delta = 1e-7
    return -np.sum(np.log(y[np.arange(batch_size), t] + delta)) / batch_size


__all__ = ["sigmoid", "softmax", "cross_entropy_error"]
