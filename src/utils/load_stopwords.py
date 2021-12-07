def load_stopwords(path: str) -> dict:
    stopwords = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            stopword = line.strip()
            stopwords.add(stopword)
    return stopwords