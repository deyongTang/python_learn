import json

file_path = '/Users/deyong/PycharmProjects/python_learn/seq.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# New cells to insert
new_cells = [
    {
        "cell_type": "markdown",
        "id": "range_intro_md",
        "metadata": {},
        "source": [
            "## Range 范围\n",
            "`range` 是一个不可变的序列类型，用于生成数字序列，常用于 `for` 循环。它非常节省内存，因为它只存储 start、stop 和 step 值，而不是整个序列。"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "range_examples_code",
        "metadata": {},
        "outputs": [],
        "source": [
            "# 1. 基本用法\n",
            "print(\"range(5):\", list(range(5)))        # [0, 1, 2, 3, 4] (默认从0开始)\n",
            "print(\"range(2, 7):\", list(range(2, 7)))     # [2, 3, 4, 5, 6] (左闭右开)\n",
            "print(\"range(1, 10, 2):\", list(range(1, 10, 2))) # [1, 3, 5, 7, 9] (步长为2)\n",
            "\n",
            "# 2. 负数步长\n",
            "print(\"range(5, 0, -1):\", list(range(5, 0, -1))) # [5, 4, 3, 2, 1]\n",
            "\n",
            "# 3. 内存高效\n",
            "# range 对象不存储所有数字，只存储 start, stop, step\n",
            "r = range(1000000)\n",
            "print(\"Length of range(1000000):\", len(r))  # 1000000\n",
            "print(\"r[100]:\", r[100])  # 100 (支持索引)\n",
            "\n",
            "# 4. 判断元素是否存在\n",
            "print(\"999 in r:\", 999 in r) # True"
        ]
    }
]

# Find the index to insert (before "练习：序列自测")
insert_index = -1
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'markdown' and '练习：序列自测' in ''.join(cell['source']):
        insert_index = i
        break

if insert_index != -1:
    # Insert before the exercise section
    notebook['cells'][insert_index:insert_index] = new_cells
    print(f"Inserted {len(new_cells)} cells at index {insert_index}")
else:
    # Append to the end if not found
    notebook['cells'].extend(new_cells)
    print("Appended cells to the end")

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("Successfully updated seq.ipynb")
