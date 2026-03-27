from DataPreparation import *

if __name__ == '__main__':
    syllabified_condition_a = syllabify_list(condition_a)
    print(syllabified_condition_a)
    stream = build_continuous_speech_stream(syllabified_condition_a, num_words=180)
    #print(stream[:24])