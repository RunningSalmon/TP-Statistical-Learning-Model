from DataPreparation import *
from StatisticalTraining import *
from Evaluation import *

if __name__ == '__main__':
    syllabified_condition_a = syllabify_list(condition_a)
    #print(syllabified_condition_a)
    stream = build_continuous_speech_stream(syllabified_condition_a, num_words=180)
    #print(stream[:24])
    TPs = find_TP(stream)
    #print(TPs)
    word_stream = separate_stream_using_tps(stream, TPs)
    print(f"{int(evaluate_accuracy(word_stream)*100)}% accuracy")