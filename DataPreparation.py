
import random


# training stimuli from Saffran et al.
condition_a = ["tupiro", "golabu", "bidaku", "padoti"]
condition_b = ["dapiku", "tilado", "burobi", "pagotu"]

# test stimuli (2 "words", 2 "non-words" depending on condition)
stimuli_test = ["tupiro", "golabu", "dapiku", "tilado"]

# Split words into a list of syllables
def syllabify(word, n=2) -> list[str]:
    result = []
    for i in range(0, len(word), n):
        result.append(word[i:i + n])

    return result

def syllabify_list(words: list[str]) -> list[str]:
    result = []
    for word in words:
        result.append(syllabify(word))

    return result

# create the training stimulus consisting of n "words"
def build_continuous_speech_stream(syllabified_words: list[list[str]], num_words: int, seed = None) -> list[list[str]]:
    if seed is not None:
        random.seed(seed)
    stream = []
    last = None
    for _ in range(num_words):
        available_words = [word for word in syllabified_words if word != last]
        choice = random.choice(available_words)
        stream.extend(choice)
        last = choice

    return stream

