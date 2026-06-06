from pathlib import Path
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


path = Path(__file__).resolve().parent.parent / "cet 6" / "_analysis_output" / "section_b_texts" / "2022.06六级真题第1套【可复制可搜索，打印首选】.txt"
text = path.read_text(encoding="utf-8")

QUESTION_RE = re.compile(r"\b(3[6-9]|4[0-5])\.\s*(.+?)(?=(?:\b(?:3[6-9]|4[0-5])\.)|$)", re.S)
PARAGRAPH_RE = re.compile(r"([A-K])\)\s*(.+?)(?=(?:\b[A-K]\))|(?:\b(?:3[6-9]|4[0-5])\.)|$)", re.S)


def norm(s: str) -> str:
    s = s.lower()
    s = s.replace("—", "-").replace("–", "-")
    s = re.sub(r"[\W_]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


paras = [(a, norm(b)) for a, b in PARAGRAPH_RE.findall(text)]
qs = [(int(a), norm(b)) for a, b in QUESTION_RE.findall(text)]

for qno, q in qs:
    docs = [q] + [p for _, p in paras]
    vec1 = TfidfVectorizer(ngram_range=(1, 3), stop_words="english").fit_transform(docs)
    vec2 = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5)).fit_transform(docs)
    s1 = cosine_similarity(vec1[0:1], vec1[1:]).ravel()
    s2 = cosine_similarity(vec2[0:1], vec2[1:]).ravel()
    scores = 0.6 * s1 + 0.4 * s2
    ranked = sorted(zip(paras, scores), key=lambda x: x[1], reverse=True)
    print("Q", qno, ranked[:3])
