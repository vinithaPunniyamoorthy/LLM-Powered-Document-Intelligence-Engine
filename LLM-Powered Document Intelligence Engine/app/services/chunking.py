def split_text(text: str, chunk_size: int = 800, chunk_overlap: int = 150):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(len(words), start + chunk_size)
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - chunk_overlap
        if start < 0:
            start = 0

    return chunks
