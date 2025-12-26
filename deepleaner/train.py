import numpy as np
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from deepleaner.common.function import softmax, sigmoid


# 784 维


def init_network():
    ## 加载模型
    network = joblib.load("data/nn_sample")
    return network


def get_data():
    data = pd.read_csv("data/train.csv")

    X = data.drop(
        "label", axis=1
    )

    y = data["label"]
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    preprocessor = MinMaxScaler()
    x_train = preprocessor.fit_transform(x_train)
    x_test = preprocessor.transform(x_test)
    return x_test, y_test


def predict(network, x):
    w1, w2, w3 = network["W1"], network["W2"], network["W3"]
    b1, b2, b3 = network["b1"], network["b2"], network["b3"]

    a1 = np.dot(x, w1) + b1
    z1 = sigmoid(a1)
    a2 = np.dot(z1, w2) + b2
    z2 = sigmoid(a2)
    a3 = np.dot(z2, w3) + b3
    y = softmax(a3)
    return y


if __name__ == "__main__":
    x, t = get_data()
    network = init_network()

    batch_size = 100  # 批数量
    accuracy_cnt = 0

    for i in range(0, len(x), batch_size):
        x_batch = x[i: i + batch_size]
        y_batch = predict(network, x_batch)
        ## 预测
        p = np.argmax(y_batch, axis=1)
        accuracy_cnt += np.sum(p == t[i: i + batch_size])

    print("Accuracy:", str(float(accuracy_cnt) / len(x)))
