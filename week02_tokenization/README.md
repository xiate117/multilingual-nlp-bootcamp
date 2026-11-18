# Week 02：多语种 Tokenization

本实验比较 mBERT、XLM-R 和 SentencePiece 的五语种切分结果，并训练一个
8,000 词 BPE 小词表。

## 运行

```powershell
cd week02_tokenization
python -m pip install -r requirements.txt
python week02_tokenization.py
```

## 目录

- `data/`：五语种各 500 句、20 个长词例句；
- `models/`：本地 mBERT 和 XLM-R tokenizer；
- `outputs/`：汇总 CSV、10 个案例、柱状图和 8k 模型；
- `report/实验报告.md`：简短实验过程和结果说明。

## 指标

- fertility = token 数 ÷ 词数；
- 序列扩张率 = token 数 ÷ 非空白字符数。

详细数据说明见 `data/README.md`。

## Windows 常见错误

若出现 `_sentencepiece` DLL 被应用程序控制策略阻止，通常是误装了 0.2.3：

```powershell
python -m pip install --force-reinstall sentencepiece==0.2.1
python -m pip install -r requirements.txt
```
