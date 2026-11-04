"""读取五语种文本，训练 Word2Vec，并输出 5 组近邻词。"""

from __future__ import annotations

import csv
import re
import unicodedata
from collections import Counter
from pathlib import Path

from gensim.models import Word2Vec


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

LANGUAGES = [
    {"code": "zh", "name": "中文", "file": "chinese.txt", "query": "语言"},
    {"code": "kk", "name": "哈萨克语", "file": "kazakh.txt", "query": "тіл"},
    {"code": "ky", "name": "柯尔克孜语", "file": "kyrgyz.txt", "query": "тил"},
    {"code": "uz", "name": "乌兹别克语", "file": "uzbek.txt", "query": "til"},
    {"code": "tr", "name": "土耳其语", "file": "turkish.txt", "query": "dil"},
]

WORD_RE = re.compile(r"[^\W_]+(?:'[^\W_]+)*", re.UNICODE)
APOSTROPHES = str.maketrans(
    {"\u02bb": "'", "\u02bc": "'", "\u2018": "'", "\u2019": "'"}
)


def tokenize(line: str, language_code: str) -> list[str]:
    """把一行文本切分为规范化后的词。"""

    text = unicodedata.normalize("NFKC", line).translate(APOSTROPHES).casefold()
    if language_code == "zh":
        return [token for token in text.split() if WORD_RE.fullmatch(token)]
    return WORD_RE.findall(text)


def read_sentences(language: dict[str, str]) -> list[list[str]]:
    """读取 UTF-8 文本并完成分词。"""

    path = DATA_DIR / language["file"]
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path} 不是有效的 UTF-8 文本") from exc

    sentences = [tokenize(line, language["code"]) for line in lines if line.strip()]
    return [sentence for sentence in sentences if sentence]


def save_frequencies(language: dict[str, str], sentences: list[list[str]]) -> None:
    """保存一种语言的完整词频表。"""

    counts = Counter(word for sentence in sentences for word in sentence)
    path = OUTPUT_DIR / f"word_frequencies_{language['code']}.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["rank", "word", "count"])
        for rank, (word, count) in enumerate(counts.most_common(), 1):
            writer.writerow([rank, word, count])


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    models: dict[str, Word2Vec] = {}

    print("========== 词频统计与 Word2Vec 训练 ==========")
    for language in LANGUAGES:
        sentences = read_sentences(language)
        save_frequencies(language, sentences)

        model = Word2Vec(
            sentences=sentences,
            vector_size=100,
            window=5,
            min_count=2,
            sg=1,
            epochs=20,
            workers=1,
            seed=42,
        )
        model.save(str(OUTPUT_DIR / f"word2vec_{language['code']}.model"))
        models[language["code"]] = model

        word_count = sum(len(sentence) for sentence in sentences)
        print(
            f"{language['name']}: {len(sentences)} 句, "
            f"{word_count} 个词, {len(model.wv)} 个词向量"
        )

    print()
    print("========== 5 组近邻词查询（most_similar） ==========")
    rows: list[dict[str, object]] = []
    for language in LANGUAGES:
        query = language["query"]
        model = models[language["code"]]
        print(f"{language['name']}: {query}")

        if query not in model.wv:
            print("    该词不在词表中")
            print()
            continue

        for rank, (neighbor, similarity) in enumerate(
            model.wv.most_similar(query, topn=5), 1
        ):
            print(f"    {neighbor:<15} {similarity:.4f}")
            rows.append(
                {
                    "language": language["name"],
                    "query": query,
                    "rank": rank,
                    "neighbor": neighbor,
                    "similarity": f"{similarity:.4f}",
                }
            )
        print()

    path = OUTPUT_DIR / "neighbor_query_results.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["language", "query", "rank", "neighbor", "similarity"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"结果目录：{OUTPUT_DIR}")


if __name__ == "__main__":
    main()
