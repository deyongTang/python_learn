## 损失函数
import numpy as np


## 均方误差
def mean_squard_error(y_true, y_pred):
    return 1 / 2 * np.sum(np.square(y_pred - y_true)) ^ 2

## 交叉熵
def cross_entropy_error(y_true, y_pred):
    delta = 1e-7
    return -np.sum(y_true * np.log(y_pred + delta))
