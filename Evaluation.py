
def separate_stream_using_tps(stream: list[str], tps: dict) -> list[str]:
    """calculates a threshold for which syllables to combine into a word
     and separates the syllable stream according to the tps and the calculated threshold
     :returns: a new stream, separated in words instead of syllables"""
    word_list = []


    #calculate mean as threshold
    summed_probability = sum(probability for (_, _), probability in tps.items())
    tp_threshold = summed_probability / len(tps)

    word = ""
    word += stream[0]
    for i in range(len(stream)-1):
        if (stream[i], stream[i+1]) not in tps or tps[stream[i], stream[i+1]] < tp_threshold:
            word_list.append(word)
            word = stream[i+1]
        else:
            word += stream[i+1]

    return word_list

def evaluate_accuracy(word_list: list[str], training_set: list[str]) -> float:
    correct = 0
    for word in word_list:
        if word in training_set:
            correct += 1

    return correct / len(word_list)