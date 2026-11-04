# Week 01：多语言 Word2Vec

数据已经放在 `data/` 中，代码只读取文本，不包含生成语料的过程。程序会完成
词频统计、Word2Vec 训练，并打印 5 组近邻词。

## 环境

- Python 3.10 或更高版本
- gensim

```powershell
cd week01_embeddings
python -m pip install -r requirements.txt
```

## 运行

```powershell
python week01_embeddings.py
```

终端会显示类似下面的内容，每种语言显示 1 个查询词的 5 个近邻：

```text
========== 5 组近邻词查询（most_similar） ==========
中文: 语言
    文字              0.9123
    文化              0.9012
    学习              0.8750
    中国              0.8421
    学生              0.8210
```

示例数字只表示显示格式，实际的词和相似度由本次训练结果决定。查询词可在
`week01_embeddings.py` 的 `LANGUAGES` 中修改。

## 数据文件

五种语言各有 2,000 行 UTF-8 文本：

| 语言 | 文件 |
|---|---|
| 中文 | `data/chinese.txt` |
| 哈萨克语 | `data/kazakh.txt` |
| 柯尔克孜语 | `data/kyrgyz.txt` |
| 乌兹别克语 | `data/uzbek.txt` |
| 土耳其语 | `data/turkish.txt` |

`data/high_frequency_examples_100.csv` 是附带的 100 个高频词示例。

## 输出

- `outputs/word_frequencies_<语言>.csv`：词频统计
- `outputs/word2vec_<语言>.model`：Word2Vec 模型
- `outputs/neighbor_query_results.csv`：5 组，每组 5 个近邻及相似度
- `report/实验报告.md`：实验报告

五种语言分别训练。没有跨语言对齐数据时，不同语言的词向量不能直接比较。
