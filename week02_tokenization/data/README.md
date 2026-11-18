# Week 2 数据

## 评估数据

`sample_500_zh.txt`、`sample_500_kk.txt`、`sample_500_ky.txt`、
`sample_500_uz.txt`、`sample_500_tr.txt` 分别包含中文、哈萨克语、柯尔克孜语、
乌兹别克语、土耳其语各 500 句。全部从 Week 1 语料按固定间隔抽取。

`long_word_examples_20.csv` 是自行整理的 20 个长词形例句，其中哈萨克语 7 句、
柯尔克孜语 7 句、乌兹别克语 6 句。每句标记一个长词，用于观察黏着语词形的
subword 切分。

## SentencePiece 训练补充文本

`sentencepiece_training/` 中每种语言有 2,000 句补充文本，来源为
Hugging Face 数据集 `Helsinki-NLP/opus-100` 的英-本语言平行语料，仅抽取本语言
一侧。补充文本只用于训练 8,000 小词表，不参与 500 句评估统计。
数据集页面：<https://huggingface.co/datasets/Helsinki-NLP/opus-100>。

如果只用 Week 1 的模板语料，SentencePiece 可达到的词表规模会明显小于 8,000；
加入 10,000 句公开文本后，训练词表实际为 8,000。
