"""Week 2: compare multilingual tokenizers and train an 8k SentencePiece model."""

from __future__ import annotations

import csv
import os
import re
import tempfile
from pathlib import Path
from statistics import mean

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "week02_mpl_cache")
)
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")

import matplotlib
import sentencepiece as spm
from transformers import AutoTokenizer

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "outputs"

LANGUAGES = [
    {"code": "zh", "name": "中文", "file": "sample_500_zh.txt"},
    {"code": "kk", "name": "哈萨克语", "file": "sample_500_kk.txt"},
    {"code": "ky", "name": "柯尔克孜语", "file": "sample_500_ky.txt"},
    {"code": "uz", "name": "乌兹别克语", "file": "sample_500_uz.txt"},
    {"code": "tr", "name": "土耳其语", "file": "sample_500_tr.txt"},
]

TOKENIZER_NAMES = ("mBERT", "XLM-R", "SentencePiece-BPE-8k")
WORD_RE = re.compile(r"[^\W_]+(?:['’][^\W_]+)*", re.UNICODE)


def read_lines(path: Path) -> list[str]:
    """Read non-empty UTF-8 lines."""

    return [
        line.strip()
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def word_count(text: str, language_code: str) -> int:
    """Count pre-segmented Chinese words or Unicode words in other languages."""

    if language_code == "zh":
        return len(text.split())
    return len(WORD_RE.findall(text))


def char_count(text: str) -> int:
    """Count non-whitespace Unicode characters."""

    return len(re.sub(r"\s+", "", text))


def load_evaluation_data() -> dict[str, list[str]]:
    """Load exactly 500 fixed sentences for each language."""

    result: dict[str, list[str]] = {}
    for language in LANGUAGES:
        lines = read_lines(DATA_DIR / language["file"])
        if len(lines) != 500:
            raise ValueError(
                f"{language['file']} 应有 500 句，实际为 {len(lines)} 句"
            )
        result[language["code"]] = lines
    return result


def load_long_examples() -> list[dict[str, str]]:
    """Load the 20 long-word examples."""

    with (DATA_DIR / "long_word_examples_20.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 20:
        raise ValueError(f"长词形示例应有 20 条，实际为 {len(rows)} 条")
    return rows


def train_sentencepiece() -> spm.SentencePieceProcessor:
    """Train a deterministic 8k BPE vocabulary."""

    output_prefix = OUTPUT_DIR / "sentencepiece_bpe_8k"
    training_files = [
        DATA_DIR / "sentencepiece_training" / f"supplement_2000_{code}.txt"
        for code in ("zh", "kk", "ky", "uz", "tr")
    ]
    spm.SentencePieceTrainer.train(
        input=",".join(str(path) for path in training_files),
        model_prefix=str(output_prefix),
        vocab_size=8000,
        model_type="bpe",
        character_coverage=0.9995,
        pad_id=0,
        unk_id=1,
        bos_id=2,
        eos_id=3,
        user_defined_symbols=["<mask>"],
        hard_vocab_limit=True,
        shuffle_input_sentence=False,
        num_threads=1,
        minloglevel=2,
    )
    processor = spm.SentencePieceProcessor(
        model_file=str(output_prefix) + ".model"
    )
    if processor.get_piece_size() != 8000:
        raise RuntimeError(
            f"SentencePiece 词表大小异常：{processor.get_piece_size()}"
        )
    return processor


def pieces_for(
    tokenizer_name: str, tokenizer, text: str
) -> tuple[list[str], int]:
    """Return token strings and the number of unknown tokens."""

    if tokenizer_name == "SentencePiece-BPE-8k":
        pieces = tokenizer.encode(text, out_type=str)
        ids = tokenizer.encode(text, out_type=int)
        unknown = sum(token_id == tokenizer.unk_id() for token_id in ids)
        return pieces, unknown

    pieces = tokenizer.tokenize(text)
    ids = tokenizer.encode(text, add_special_tokens=False)
    unknown = sum(token_id == tokenizer.unk_token_id for token_id in ids)
    return pieces, unknown


def display_pieces(pieces: list[str]) -> str:
    """Escape a token list for Markdown."""

    escaped = [piece.replace("|", "\\|").replace("`", "'") for piece in pieces]
    return "`" + " | ".join(escaped) + "`"


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    evaluation_data = load_evaluation_data()
    long_examples = load_long_examples()

    print("加载本地 mBERT 和 XLM-R tokenizer...")
    mbert = AutoTokenizer.from_pretrained(
        str(MODEL_DIR / "mbert_tokenizer"),
        local_files_only=True,
        use_fast=True,
    )
    xlmr = AutoTokenizer.from_pretrained(
        str(MODEL_DIR / "xlmr_tokenizer"),
        local_files_only=True,
        use_fast=True,
    )

    print("训练 8k SentencePiece BPE 词表...")
    sentencepiece = train_sentencepiece()
    tokenizers = {
        "mBERT": mbert,
        "XLM-R": xlmr,
        "SentencePiece-BPE-8k": sentencepiece,
    }

    summary_rows: list[dict[str, object]] = []

    for language in LANGUAGES:
        code = language["code"]
        for tokenizer_name, tokenizer in tokenizers.items():
            per_sentence: list[dict[str, float]] = []
            for text in evaluation_data[code]:
                pieces, unknown = pieces_for(tokenizer_name, tokenizer, text)
                words = word_count(text, code)
                chars = char_count(text)
                token_count = len(pieces)
                fertility = token_count / words if words else 0.0
                expansion = token_count / chars if chars else 0.0
                per_sentence.append(
                    {
                        "tokens": token_count,
                        "words": words,
                        "characters": chars,
                        "fertility": fertility,
                        "expansion": expansion,
                        "unknown": unknown,
                    }
                )

            total_tokens = sum(row["tokens"] for row in per_sentence)
            total_unknown = sum(row["unknown"] for row in per_sentence)
            avg_tokens = mean(row["tokens"] for row in per_sentence)
            avg_fertility = mean(
                row["fertility"] for row in per_sentence
            )
            summary_rows.append(
                {
                    "language": language["name"],
                    "language_code": code,
                    "tokenizer": tokenizer_name,
                    "sentences": len(per_sentence),
                    "avg_tokens": round(avg_tokens, 4),
                    "avg_words": round(
                        mean(row["words"] for row in per_sentence), 4
                    ),
                    "avg_characters": round(
                        mean(row["characters"] for row in per_sentence), 4
                    ),
                    "fertility": round(avg_fertility, 4),
                    "sequence_expansion_rate": round(
                        mean(row["expansion"] for row in per_sentence), 4
                    ),
                    "unknown_rate": round(total_unknown / total_tokens, 6)
                    if total_tokens
                    else 0.0,
                }
            )
            print(
                f"{language['name']:<5} {tokenizer_name:<23} "
                f"tokens={avg_tokens:7.2f} fertility={avg_fertility:6.3f}"
            )

    summary_fields = [
        "language",
        "language_code",
        "tokenizer",
        "sentences",
        "avg_tokens",
        "avg_words",
        "avg_characters",
        "fertility",
        "sequence_expansion_rate",
        "unknown_rate",
    ]
    with (OUTPUT_DIR / "tokenizer_summary.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary_rows)

    long_rows: list[dict[str, object]] = []
    for row in long_examples:
        output_row: dict[str, object] = {
            "id": row["id"],
            "language": row["language_label"],
            "sentence": row["sentence"],
            "long_word": row["long_word"],
            "char_length": len(row["long_word"]),
        }
        for tokenizer_name, tokenizer in tokenizers.items():
            pieces, unknown = pieces_for(
                tokenizer_name, tokenizer, row["long_word"]
            )
            key = {
                "mBERT": "mbert",
                "XLM-R": "xlmr",
                "SentencePiece-BPE-8k": "sentencepiece",
            }[tokenizer_name]
            output_row[f"{key}_pieces"] = " | ".join(pieces)
            output_row[f"{key}_count"] = len(pieces)
            output_row[f"{key}_unknown"] = unknown
        long_rows.append(output_row)

    long_fields = [
        "id",
        "language",
        "sentence",
        "long_word",
        "char_length",
        "mbert_pieces",
        "mbert_count",
        "mbert_unknown",
        "xlmr_pieces",
        "xlmr_count",
        "xlmr_unknown",
        "sentencepiece_pieces",
        "sentencepiece_count",
        "sentencepiece_unknown",
    ]
    with (OUTPUT_DIR / "long_word_tokenization.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=long_fields)
        writer.writeheader()
        writer.writerows(long_rows)

    case_lines = ["# 10 组可解释切分案例", ""]
    selected_case_indexes = [0, 2, 4, 7, 9, 12, 14, 15, 17, 19]
    for row in [long_rows[index] for index in selected_case_indexes]:
        case_lines.extend(
            [
                f"## {row['id']}. {row['language']}：`{row['long_word']}`",
                "",
                f"原句：{row['sentence']}",
                "",
                f"- mBERT：{display_pieces(str(row['mbert_pieces']).split(' | '))}",
                f"- XLM-R：{display_pieces(str(row['xlmr_pieces']).split(' | '))}",
                "- SentencePiece-BPE-8k："
                f"{display_pieces(str(row['sentencepiece_pieces']).split(' | '))}",
                "",
                f"切分数量：mBERT {row['mbert_count']}，"
                f"XLM-R {row['xlmr_count']}，"
                f"SentencePiece {row['sentencepiece_count']}。",
                "",
            ]
        )
    (OUTPUT_DIR / "case_studies_10.md").write_text(
        "\n".join(case_lines), encoding="utf-8", newline="\n"
    )

    labels = [language["code"] for language in LANGUAGES]
    x_positions = list(range(len(labels)))
    width = 0.24
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for index, tokenizer_name in enumerate(TOKENIZER_NAMES):
        values = [
            next(
                row["fertility"]
                for row in summary_rows
                if row["language_code"] == code
                and row["tokenizer"] == tokenizer_name
            )
            for code in labels
        ]
        offsets = [position + (index - 1) * width for position in x_positions]
        ax.bar(offsets, values, width, label=tokenizer_name)

    ax.set_title("Fertility by language and tokenizer")
    ax.set_xlabel("Language")
    ax.set_ylabel("Subword tokens / word")
    ax.set_xticks(x_positions, labels)
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "fertility_comparison.png", dpi=180)
    plt.close(fig)

    print(f"完成，结果目录：{OUTPUT_DIR}")


if __name__ == "__main__":
    main()
