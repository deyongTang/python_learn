from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from deepleaner.common.functions import sigmoid, softmax, cross_entropy_error
from deepleaner.common.gradient import numerical_gradient


# 读入数据

def get_data(csv_path=None, test_ratio=0.2, max_samples=None):
    """
    读取 train.csv，并划分训练集/测试集。
    - 第 1 列是标签
    - 后 784 列是像素
    """
    if csv_path is None:
        base_dir = Path(__file__).resolve().parents[1]
        csv_path = base_dir / "data" / "train.csv"

    df = pd.read_csv(csv_path)
    if max_samples is not None:
        df = df.iloc[:max_samples]

    x = df.drop("label", axis=1).to_numpy(dtype=np.float32) / 255.0
    t = df["label"].to_numpy()

    # 打乱
    idx = np.random.permutation(len(x))
    x = x[idx]
    t = t[idx]

    # 划分
    split = int(len(x) * (1 - test_ratio))
    x_train, x_test = x[:split], x[split:]
    t_train, t_test = t[:split], t[split:]

    return x_train, x_test, t_train, t_test


class TwoLayerNet:
    def __init__(self, input_size, hidden_size, output_size, weight_init_std=0.01):
        # 初始化权重
        self.params = {}
        self.params["W1"] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params["b1"] = np.zeros(hidden_size)
        self.params["W2"] = weight_init_std * np.random.randn(hidden_size, output_size)
        self.params["b2"] = np.zeros(output_size)

    def predict(self, x):
        W1, W2 = self.params["W1"], self.params["W2"]
        b1, b2 = self.params["b1"], self.params["b2"]

        a1 = np.dot(x, W1) + b1
        z1 = sigmoid(a1)
        a2 = np.dot(z1, W2) + b2
        y = softmax(a2)
        return y

    # x: 输入数据, t: 监督数据
    def loss(self, x, t):
        y = self.predict(x)
        return cross_entropy_error(y, t)

    def accuracy(self, x, t):
        y = self.predict(x)
        y = np.argmax(y, axis=1)
        t = t.reshape(-1)

        accuracy = np.sum(y == t) / float(x.shape[0])
        return accuracy

    # x: 输入数据, t: 监督数据
    def numerical_gradient(self, x, t):
        # W will be modified in-place by numerical_gradient, and self.loss reads self.params.
        loss_W = lambda W: self.loss(x, t)

        grads = {}
        grads["W1"] = numerical_gradient(loss_W, self.params["W1"])
        grads["b1"] = numerical_gradient(loss_W, self.params["b1"])
        grads["W2"] = numerical_gradient(loss_W, self.params["W2"])
        grads["b2"] = numerical_gradient(loss_W, self.params["b2"])

        return grads

    def gradient(self, x, t):
        W1, W2 = self.params["W1"], self.params["W2"]
        b1, b2 = self.params["b1"], self.params["b2"]

        a1 = np.dot(x, W1) + b1
        z1 = sigmoid(a1)
        a2 = np.dot(z1, W2) + b2
        y = softmax(a2)

        if t.ndim != 1:
            t = np.argmax(t, axis=1)

        batch_size = x.shape[0]
        dy = y.copy()
        dy[np.arange(batch_size), t] -= 1
        dy /= batch_size

        grads = {}
        grads["W2"] = np.dot(z1.T, dy)
        grads["b2"] = np.sum(dy, axis=0)
        dz1 = np.dot(dy, W2.T)
        da1 = dz1 * z1 * (1 - z1)
        grads["W1"] = np.dot(x.T, da1)
        grads["b1"] = np.sum(da1, axis=0)

        return grads


if __name__ == "__main__":
    # 读入数据
    # 数值梯度很慢，教学演示可先设置 max_samples（如 200）
    x_train, x_test, t_train, t_test = get_data(max_samples=None)

    network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

    iters_num = 10000  # 适当设定循环的次数
    train_size = x_train.shape[0]
    batch_size = 100
    learning_rate = 0.1

    train_loss_list = []
    train_acc_list = []
    test_acc_list = []

            
    ## 取商-
    iter_per_epoch = max(train_size // batch_size, 1)

    for i in range(iters_num):
        batch_mask = np.random.choice(train_size, batch_size)
        x_batch = x_train[batch_mask]
        t_batch = t_train[batch_mask]

        # 计算梯度（反向传播；数值梯度会非常慢）
        grad = network.gradient(x_batch, t_batch)
        #grad= network.numerical_gradient(x_batch, t_batch)
        # 更新参数
        for key in ("W1", "b1", "W2", "b2"):
            ## 梯度下降法
            network.params[key] -= learning_rate * grad[key]

        loss = network.loss(x_batch, t_batch)
        train_loss_list.append(loss)

        if i % iter_per_epoch == 0:
            train_acc = network.accuracy(x_train, t_train)
            test_acc = network.accuracy(x_test, t_test)
            train_acc_list.append(train_acc)
            test_acc_list.append(test_acc)
            print("train acc, test acc | " + str(train_acc) + ", " + str(test_acc))

    # 绘制图形
    x = np.arange(len(train_acc_list))
    plt.plot(x, train_acc_list, label="train acc")
    plt.plot(x, test_acc_list, label="test acc", linestyle="--")
    plt.xlabel("epochs")
    plt.ylabel("accuracy")
    plt.ylim(0, 1.0)
    plt.legend(loc="lower right")
    plt.show()
