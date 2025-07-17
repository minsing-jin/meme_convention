# meme_convention/utils/prefix.py
from typing import Dict, List

def shortest_unique_prefixes(words: List[str]) -> Dict[str, str]:
    """
    Return a mapping word → shortest unique prefix (case preserved).
    """
    if not words:
        return {}
    lower_words = [w.lower() for w in words]
    result: Dict[str, str] = {}
    for w in lower_words:
        for i in range(1, len(w) + 1):
            prefix = w[:i]
            if sum(other.startswith(prefix) for other in lower_words) == 1:
                result[w] = prefix
                break
        else:  # identical words – fall back to full word
            result[w] = w
    # Re-map original casing
    return {orig: result[orig.lower()] for orig in words}
