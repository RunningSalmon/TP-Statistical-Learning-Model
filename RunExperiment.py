from DataPreparation import *
from StatisticalTraining import *
from Evaluation import *

def run_experiment(num_trials: int) -> (dict, dict, float):
    summed_accuracy = 0
    summed_tps_condition_a = {}
    summed_tps_condition_b = {}
    num_trials_a = 0
    num_trials_b = 0
    for i in range(num_trials):
        # --- DataPreparation ---
        #uneven numbers -> condition a, even numbers -> condition b
        b_trial = i % 2 == 0
        training_set = condition_b if b_trial else condition_a
        syllabified_training_set = syllabified_condition_b if b_trial else syllabified_condition_a
        syllable_stream = build_continuous_speech_stream(syllabified_training_set, num_words=180)
        print(f"syllable_stream in trial {i}: {syllable_stream}")

        # --- statistical analysis ---
        tps = find_tps(syllable_stream)
        print(f"tps in trial {i}: {tps}")

        # --- testing and evaluation ---
        word_stream = separate_stream_using_tps(syllable_stream, tps)
        accuracy = evaluate_accuracy(word_stream, training_set)
        print(f"accuracy on trial {i}: {accuracy}")

        # --- sum over trials ---
        summed_tps = summed_tps_condition_b if b_trial else summed_tps_condition_a
        for (a, b), probability in tps.items():
            if (a, b) not in summed_tps:
                summed_tps[(a, b)] = 0
            summed_tps[(a, b)] += probability

        summed_accuracy += accuracy

        if b_trial:
            num_trials_a += 1
        else:
            num_trials_b += 1

    average_tps_a = {}
    average_tps_b = {}
    for (a, b), probability in summed_tps_condition_a.items():
        average_tps_a[(a, b)] = summed_tps_condition_a[(a, b)] / num_trials_a
    for (a, b), probability in summed_tps_condition_b.items():
        average_tps_b[(a, b)] = summed_tps_condition_b[(a, b)] / num_trials_b

    average_accuracy = summed_accuracy / num_trials

    return  average_tps_a, average_tps_b, average_accuracy


if __name__ == '__main__':
    overall_tps_a, overall_tps_b, overall_accuracy = run_experiment(num_trials=24)
    print(f"overall_accuracy on 24 trials: {overall_accuracy}")
    print(f"overall_tps on 24 trials: {overall_tps_a, overall_tps_b}")