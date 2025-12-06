# Range 函数使用详解

`range` 是 Python 中一个非常有用的内置函数，用于生成数字序列。它返回的是一个不可变的序列类型。

## 1. 基本用法

`range()` 函数可以接收 1 到 3 个参数：

- `range(stop)`: 生成 0 到 stop-1 的序列
- `range(start, stop)`: 生成 start 到 stop-1 的序列
- `range(start, stop, step)`: 以 step 为步长生成序列

```python
# 1. 只有一个参数 (结束值)
# 生成 0, 1, 2, 3, 4
print(list(range(5))) 

# 2. 两个参数 (起始值, 结束值)
# 生成 2, 3, 4, 5, 6 (不包含 7)
print(list(range(2, 7)))

# 3. 三个参数 (起始值, 结束值, 步长)
# 生成 1, 3, 5, 7, 9
print(list(range(1, 10, 2)))
```

## 2. 进阶用法

### 负数步长 (递减序列)

```python
# 从 5 倒数到 1
print(list(range(5, 0, -1))) # [5, 4, 3, 2, 1]
```

### 内存高效

`range` 对象非常节省内存。无论序列多长，它只存储 start, stop, step 三个值。只有在迭代或索引访问时才计算具体的数值。

```python
r = range(1000000)
print(len(r))  # 1000000
print(r[100])  # 100 (支持索引访问)
```

### 判断元素是否存在

可以使用 `in` 关键字快速检查某个数字是否在 range 中。

```python
r = range(0, 100, 2)
print(50 in r)  # True
print(51 in r)  # False
```

### 在 for 循环中使用

这是 range 最常见的用途。

```python
for i in range(3):
    print(f"Loop {i}")
```
