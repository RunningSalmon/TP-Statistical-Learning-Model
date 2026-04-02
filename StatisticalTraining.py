
def calculate_unigram_bigram_counts(speech_stream: list[str]):
    unigram_counts = {}
    bigram_counts = {}
    for i in range(len(speech_stream) - 1):
        # count general quantity
        syllable = speech_stream[i]
        if syllable not in unigram_counts:
            unigram_counts[syllable] = 0
        unigram_counts[syllable] += 1

        # count co-occurrence
        next_syllable = speech_stream[i + 1]
        if (syllable, next_syllable) not in bigram_counts:
            bigram_counts[syllable, next_syllable] = 0
        bigram_counts[syllable, next_syllable] += 1

    return unigram_counts, bigram_counts

def find_tps(speech_stream: list[str]) -> dict:
    """calculates the probability of syllable a being followed by syllable b
    :returns: a dict in which the probability of a being followed by b is denoted in dict[(a,b)]"""
    unigram_counts, bigram_counts = calculate_unigram_bigram_counts(speech_stream)

    TPs = {}

    for (a,b), count in bigram_counts.items():
        TPs[(a,b)] = count/unigram_counts[a]

    return TPs