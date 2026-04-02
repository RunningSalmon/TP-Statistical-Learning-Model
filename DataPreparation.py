
import random


# training stimuli from Saffran et al.
ex1_condition_a = ["tupiro", "golabu", "bidaku", "padoti"]
ex1_condition_b = ["dapiku", "tilado", "burobi", "pagotu"]

# training stimuli from Aslin et al.
ex2_condition_a = ["pabiku", "tibudo", "golatu", "daropi"]
ex2_condition_b = ["tudaro", "pigola", "bikuti", "budopa"]

def pick_training_set_from_expnr(expnr: int) -> tuple[list, list, list]:
    """pick training set from given expnr
    :returns: training set a, b, the weight vector and the test-set"""
    weight_vec = None
    match expnr:
        case 0:
            condition_a, condition_b = ex1_condition_a, ex1_condition_b
        case 1:
            condition_a, condition_b = ex2_condition_a, ex2_condition_b
            weight_vec = [1, 1, 2, 2]
        case _:
            raise ValueError(f"{expnr} is not a valid experiment nr. Check Readme.md for details")

    return condition_a, condition_b, weight_vec


# Split words into a list of syllables
def syllabify(word, n=2) -> list[str]:
    result = []
    for i in range(0, len(word), n):
        result.append(word[i:i + n])

    return result

def syllabify_list(words: list[str]) -> list[list[str]]:
    result = []
    for word in words:
        result.append(syllabify(word))

    return result

ex1_syllabified_condition_a = syllabify_list(ex1_condition_a)
ex1_syllabified_condition_b = syllabify_list(ex1_condition_b)
ex2_syllabified_condition_a = syllabify_list(ex2_condition_a)
ex2_syllabified_condition_b = syllabify_list(ex2_condition_b)

# create the training stimulus consisting of n "words"
def build_continuous_speech_stream(syllabified_words: list[list[str]], num_words: int, seed = None, weight_vec = None) -> list[str]:
    if seed is not None:
        random.seed(seed)
    if weight_vec is not None:
        if len(syllabified_words) != len(weight_vec):
            raise ValueError("weight vector must be same length as syllabified word list")
    else:
        # build a weight vector with equal probabilities
        weight_vec = [1] * len(syllabified_words)

    stream = []
    last_idx = None
    for _ in range(num_words):
        # set probability of word picked previously to 0
        current_weight_vec = [
            0 if i == last_idx else w for i, w in enumerate(weight_vec)
        ]
        choice = random.choices(syllabified_words, weights=current_weight_vec, k=1)[0]
        stream.extend(choice)
        last_idx = syllabified_words.index(choice)

    return stream

