# PyTorch 学习指南

## 目录
1. [PyTorch 简介](#pytorch-简介)
2. [安装与环境配置](#安装与环境配置)
3. [张量基础](#张量基础)
4. [自动微分](#自动微分)
5. [构建神经网络](#构建神经网络)
6. [训练模型](#训练模型)
7. [数据加载与处理](#数据加载与处理)
8. [模型保存与加载](#模型保存与加载)
9. [实战案例](#实战案例)
10. [最佳实践](#最佳实践)

---

## PyTorch 简介

PyTorch 是一个开源的深度学习框架，由 Facebook AI Research 开发。它具有以下特点：

- **动态计算图**：灵活且易于调试
- **Python 优先**：原生 Python 接口，易于学习
- **强大的 GPU 加速**：无缝支持 CUDA
- **丰富的生态系统**：torchvision、torchtext、torchaudio 等

---

## 安装与环境配置

### 基础安装

```bash
# CPU 版本
pip install torch torchvision torchaudio

# GPU 版本 (CUDA 11.8)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# GPU 版本 (CUDA 12.1)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 验证安装

```python
import torch

print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 是否可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA 版本: {torch.version.cuda}")
    print(f"GPU 设备数量: {torch.cuda.device_count()}")
    print(f"当前 GPU: {torch.cuda.get_device_name(0)}")
```

---

## 张量基础

### 创建张量

```python
import torch

# 从列表创建
tensor_from_list = torch.tensor([1, 2, 3, 4])

# 创建特殊张量
zeros = torch.zeros(3, 4)  # 全零张量
ones = torch.ones(2, 3)    # 全一张量
random = torch.rand(2, 3)  # 随机张量 [0, 1)
randn = torch.randn(2, 3)  # 标准正态分布

# 指定数据类型和设备
tensor = torch.tensor([1.0, 2.0], dtype=torch.float32, device='cuda')

# 从 NumPy 数组创建
import numpy as np
np_array = np.array([1, 2, 3])
tensor_from_numpy = torch.from_numpy(np_array)
```

### 张量操作

```python
# 基本运算
a = torch.tensor([1, 2, 3])
b = torch.tensor([4, 5, 6])

c = a + b           # 加法
c = torch.add(a, b) # 等价写法
c = a * b           # 逐元素乘法
c = a @ b           # 点积

# 形状操作
x = torch.randn(2, 3, 4)
print(x.shape)              # torch.Size([2, 3, 4])
y = x.view(2, 12)           # 重塑
z = x.reshape(6, 4)         # 重塑（更灵活）
w = x.transpose(0, 1)       # 转置
v = x.permute(2, 0, 1)      # 维度重排

# 索引和切片
tensor = torch.randn(4, 5)
print(tensor[0])            # 第一行
print(tensor[:, 1])         # 第二列
print(tensor[1:3, 2:4])     # 切片

# 拼接
x = torch.randn(2, 3)
y = torch.randn(2, 3)
z = torch.cat([x, y], dim=0)  # 沿第 0 维拼接
w = torch.stack([x, y], dim=0) # 创建新维度
```

### 张量与 NumPy 互转

```python
# Tensor -> NumPy
tensor = torch.randn(2, 3)
numpy_array = tensor.numpy()

# NumPy -> Tensor
numpy_array = np.array([[1, 2], [3, 4]])
tensor = torch.from_numpy(numpy_array)

# 注意：共享内存，修改一个会影响另一个
```

---

## 自动微分

PyTorch 的自动微分系统（autograd）是其核心功能之一。

### 基础用法

```python
import torch

# 创建需要梯度的张量
x = torch.tensor([2.0], requires_grad=True)
y = torch.tensor([3.0], requires_grad=True)

# 前向传播
z = x ** 2 + y ** 3

# 反向传播
z.backward()

# 查看梯度
print(f"dz/dx = {x.grad}")  # 2*x = 4.0
print(f"dz/dy = {y.grad}")  # 3*y^2 = 27.0
```

### 梯度管理

```python
# 禁用梯度计算（推理时使用）
with torch.no_grad():
    y = x * 2

# 临时启用梯度
with torch.enable_grad():
    y = x * 2

# 清零梯度
x.grad.zero_()

# 分离计算图
y = x.detach()  # y 不再追踪梯度
```

### 高级示例

```python
# 多次反向传播
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x ** 2
z = y.sum()

z.backward()
print(x.grad)  # [2.0, 4.0, 6.0]

# 梯度累积
x.grad.zero_()
for i in range(3):
    y = (x ** 2).sum()
    y.backward()
print(x.grad)  # 累积了 3 次
```

---

## 构建神经网络

### 使用 nn.Module

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 创建模型
model = SimpleNet(784, 128, 10)
print(model)

# 查看参数
for name, param in model.named_parameters():
    print(f"{name}: {param.shape}")
```

### 常用层

```python
# 全连接层
fc = nn.Linear(in_features=100, out_features=50)

# 卷积层
conv2d = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, padding=1)

# 池化层
maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
avgpool = nn.AvgPool2d(kernel_size=2)

# 归一化层
batchnorm = nn.BatchNorm2d(64)
layernorm = nn.LayerNorm(128)

# Dropout
dropout = nn.Dropout(p=0.5)

# 激活函数
relu = nn.ReLU()
sigmoid = nn.Sigmoid()
tanh = nn.Tanh()
```

### CNN 示例

```python
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x
```

### Sequential 容器

```python
# 使用 Sequential 简化模型定义
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(256, 128),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(128, 10)
)
```

---

## 训练模型

### 完整训练流程

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# 1. 准备数据
X_train = torch.randn(1000, 784)
y_train = torch.randint(0, 10, (1000,))
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 2. 定义模型
model = SimpleNet(784, 128, 10)

# 3. 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 4. 训练循环
num_epochs = 10
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

for epoch in range(num_epochs):
    model.train()  # 设置为训练模式
    running_loss = 0.0
    
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        
        # 前向传播
        output = model(data)
        loss = criterion(output, target)
        
        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    avg_loss = running_loss / len(train_loader)
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}')
```

### 评估模型

```python
def evaluate(model, test_loader, device):
    model.eval()  # 设置为评估模式
    correct = 0
    total = 0
    
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            _, predicted = torch.max(output.data, 1)
            total += target.size(0)
            correct += (predicted == target).sum().item()
    
    accuracy = 100 * correct / total
    print(f'Accuracy: {accuracy:.2f}%')
    return accuracy
```

### 常用优化器

```python
# SGD
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Adam
optimizer = optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))

# AdamW
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)

# RMSprop
optimizer = optim.RMSprop(model.parameters(), lr=0.01, alpha=0.99)
```

### 学习率调度

```python
from torch.optim.lr_scheduler import StepLR, ReduceLROnPlateau, CosineAnnealingLR

# 每 N 个 epoch 降低学习率
scheduler = StepLR(optimizer, step_size=10, gamma=0.1)

# 根据指标自适应调整
scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=5)

# 余弦退火
scheduler = CosineAnnealingLR(optimizer, T_max=50)

# 在训练循环中使用
for epoch in range(num_epochs):
    train(...)
    val_loss = validate(...)
    scheduler.step(val_loss)  # ReduceLROnPlateau
    # scheduler.step()  # 其他调度器
```

---

## 数据加载与处理

### Dataset 和 DataLoader

```python
from torch.utils.data import Dataset, DataLoader

class CustomDataset(Dataset):
    def __init__(self, data, labels, transform=None):
        self.data = data
        self.labels = labels
        self.transform = transform
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        sample = self.data[idx]
        label = self.labels[idx]
        
        if self.transform:
            sample = self.transform(sample)
        
        return sample, label

# 使用
dataset = CustomDataset(X_train, y_train)
dataloader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,
    pin_memory=True  # GPU 加速
)
```

### 图像数据处理

```python
from torchvision import datasets, transforms

# 定义转换
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                       std=[0.229, 0.224, 0.225])
])

# 加载 MNIST 数据集
train_dataset = datasets.MNIST(
    root='./data',
    train=True,
    download=True,
    transform=transform
)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
```

### 数据增强

```python
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

test_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
```

---

## 模型保存与加载

### 保存和加载整个模型

```python
# 保存
torch.save(model, 'model.pth')

# 加载
model = torch.load('model.pth')
model.eval()
```

### 保存和加载模型参数（推荐）

```python
# 保存
torch.save(model.state_dict(), 'model_weights.pth')

# 加载
model = SimpleNet(784, 128, 10)
model.load_state_dict(torch.load('model_weights.pth'))
model.eval()
```

### 保存检查点

```python
# 保存检查点
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
    'accuracy': accuracy
}
torch.save(checkpoint, 'checkpoint.pth')

# 加载检查点
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
loss = checkpoint['loss']
```

---

## 实战案例

### 案例 1：MNIST 手写数字识别

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# 数据准备
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST('./data', train=False, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

# 模型定义
class MNISTNet(nn.Module):
    def __init__(self):
        super(MNISTNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = nn.functional.relu(x)
        x = self.conv2(x)
        x = nn.functional.relu(x)
        x = nn.functional.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = nn.functional.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        return nn.functional.log_softmax(x, dim=1)

# 训练
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MNISTNet().to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.NLLLoss()

def train_epoch(model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        
        if batch_idx % 100 == 0:
            print(f'Epoch: {epoch}, Batch: {batch_idx}, Loss: {loss.item():.6f}')

def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += criterion(output, target).item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
    
    test_loss /= len(test_loader)
    accuracy = 100. * correct / len(test_loader.dataset)
    print(f'Test Loss: {test_loss:.4f}, Accuracy: {accuracy:.2f}%')

# 运行训练
for epoch in range(1, 11):
    train_epoch(model, device, train_loader, optimizer, epoch)
    test(model, device, test_loader)
```

### 案例 2：迁移学习

```python
import torch
import torch.nn as nn
from torchvision import models, transforms

# 加载预训练模型
model = models.resnet18(pretrained=True)

# 冻结所有层
for param in model.parameters():
    param.requires_grad = False

# 替换最后一层
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 10)  # 10 个类别

# 只训练最后一层
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

# 或者微调所有层
for param in model.parameters():
    param.requires_grad = True

optimizer = optim.Adam([
    {'params': model.fc.parameters(), 'lr': 0.001},
    {'params': model.layer4.parameters(), 'lr': 0.0001},
    {'params': model.layer3.parameters(), 'lr': 0.00001}
])
```

---

## 最佳实践

### 1. 设备管理

```python
# 自动选择设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 将模型和数据移到设备
model = model.to(device)
data = data.to(device)

# 多 GPU 训练
if torch.cuda.device_count() > 1:
    model = nn.DataParallel(model)
```

### 2. 梯度裁剪

```python
# 防止梯度爆炸
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

### 3. 混合精度训练

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for data, target in train_loader:
    optimizer.zero_grad()
    
    with autocast():
        output = model(data)
        loss = criterion(output, target)
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

### 4. 早停法

```python
class EarlyStopping:
    def __init__(self, patience=7, min_delta=0):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False
    
    def __call__(self, val_loss):
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss > self.best_loss - self.min_delta:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_loss = val_loss
            self.counter = 0
```

### 5. 模型调试

```python
# 检查模型输出形状
def check_model(model, input_shape):
    x = torch.randn(input_shape)
    output = model(x)
    print(f"Input shape: {x.shape}")
    print(f"Output shape: {output.shape}")

# 查看模型参数量
def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

print(f"Total parameters: {count_parameters(model):,}")

# 检查梯度
for name, param in model.named_parameters():
    if param.grad is not None:
        print(f"{name}: grad norm = {param.grad.norm()}")
```

### 6. 可复现性

```python
import random
import numpy as np

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(42)
```

---

## 学习资源

### 官方资源
- [PyTorch 官方文档](https://pytorch.org/docs/stable/index.html)
- [PyTorch 教程](https://pytorch.org/tutorials/)
- [PyTorch 示例](https://github.com/pytorch/examples)

### 推荐课程
- Deep Learning with PyTorch (Udacity)
- PyTorch for Deep Learning (fast.ai)
- CS231n: Convolutional Neural Networks (Stanford)

### 实践项目
- 图像分类（CIFAR-10, ImageNet）
- 目标检测（YOLO, Faster R-CNN）
- 自然语言处理（BERT, GPT）
- 生成对抗网络（GAN）

---

## 总结

PyTorch 是一个强大而灵活的深度学习框架。通过本指南，你应该掌握了：

- 张量操作和自动微分
- 构建和训练神经网络
- 数据加载和预处理
- 模型保存和部署
- 实战案例和最佳实践

继续实践和探索，你将能够使用 PyTorch 构建更复杂的深度学习应用！
