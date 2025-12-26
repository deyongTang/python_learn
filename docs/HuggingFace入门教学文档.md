# Hugging Face 官方教学案例：文本情感分类（参考官方课程）

本教学文档基于 Hugging Face 官方课程与教程中的**文本分类案例**整理，目标是让你完整跑通「加载数据 → 分词 → 训练 → 评估 → 推理」的标准流程。

## 0. 你将完成的任务

使用 IMDb 影评数据集训练一个情感分类模型（正向/负向），并掌握官方推荐的 Trainer 训练流程。

## 1. 环境准备

```bash
pip install "transformers>=4.30" "datasets>=2.10" "evaluate>=0.4" "accelerate>=0.20" torch
```

说明：官方教程默认使用 PyTorch。

## 2. 加载数据集（datasets）

```python
from datasets import load_dataset

dataset = load_dataset("imdb")
print(dataset)
print(dataset["train"][0])
```

你会得到 `train/test` 两个切分，每条数据包含 `text` 与 `label`。

## 3. 分词与预处理（tokenizer + map）

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(batch):
    return tokenizer(batch["text"], truncation=True)

encoded = dataset.map(tokenize, batched=True)
```

要点：官方案例强调用 `map` 批量处理，并让 `tokenizer` 负责截断。

## 4. 动态 padding（DataCollator）

```python
from transformers import DataCollatorWithPadding

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
```

这样每个 batch 会自动补齐到当前 batch 的最长序列，速度更快、显存更省。

## 5. 构建模型（AutoModel）

```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2
)
```

## 6. 评估指标（evaluate）

```python
import evaluate

accuracy = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = logits.argmax(axis=-1)
    return accuracy.compute(predictions=predictions, references=labels)
```

## 7. 训练（TrainingArguments + Trainer）

```python
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./outputs",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=1,
    weight_decay=0.01,
    logging_steps=50,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded["train"],
    eval_dataset=encoded["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()
trainer.evaluate()
```

## 8. 推理（官方推荐 pipeline）

```python
from transformers import pipeline

clf = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
print(clf("This movie is fantastic!"))
```

## 9. 保存与上传（可选）

```python
model.save_pretrained("./imdb_sentiment")
tokenizer.save_pretrained("./imdb_sentiment")
```

上传到 Hub：

```python
from huggingface_hub import login

login()
model.push_to_hub("your-username/imdb-sentiment")
```

## 10. 常见问题与排查

- **显存不足**：减小 batch size 或使用 `distilbert`
- **训练太慢**：使用 GPU 或减少 `num_train_epochs`
- **文本太长被截断**：显式设置 `max_length`
- **精度不稳定**：提高 epoch 或调小学习率

## 11. 官方参考链接

- Hugging Face Course（文本分类章节）：https://huggingface.co/learn/nlp-course
- Transformers 训练文档：https://huggingface.co/docs/transformers/training
- Datasets 文档：https://huggingface.co/docs/datasets
- Evaluate 文档：https://huggingface.co/docs/evaluate

---

如果你希望把这个案例替换成中文任务或你的自定义数据集，我可以基于同一流程改成对应版本。
