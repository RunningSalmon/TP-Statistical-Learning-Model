import sys

from DataPreparation import *
from StatisticalTraining import *
from Evaluation import *
from VisualizeExperiment import *

def run_experiment(experiment_nr: int, num_trials: int) -> [dict, dict, dict, dict, float]:
    """runs the experiment according to the given experiment number.
    :return: average_tps_a, average_tps_b, average_bigram_count_a, average_bigram_count_b, average_accuracy"""
    summed_accuracy = 0
    summed_bigrams_condition_a = {}
    summed_bigrams_condition_b = {}
    summed_tps_condition_a = {}
    summed_tps_condition_b = {}
    num_trials_a = 0
    num_trials_b = 0
    for i in range(num_trials):
        # --- DataPreparation ---
        #pick training set and weight-vector from given experiment_nr
        condition_a, condition_b, weight_vec = pick_training_set_from_expnr(experiment_nr)

        #uneven numbers -> condition a, even numbers -> condition b
        b_trial = i % 2 == 0
        training_set = condition_b if b_trial else condition_a
        syllabified_training_set = syllabify_list(training_set)
        syllable_stream = build_continuous_speech_stream(syllabified_training_set, num_words=180, weight_vec=weight_vec)
        print(f"syllable_stream in trial {i}: {syllable_stream}")

        # --- statistical analysis ---
        unigrams, bigrams = calculate_unigram_bigram_counts(syllable_stream)
        tps = find_tps(syllable_stream)
        print(f"tps in trial {i}: {tps}")

        # --- testing and evaluation ---
        word_stream = separate_stream_using_tps(syllable_stream, tps)
        accuracy = evaluate_accuracy(word_stream, training_set)
        print(f"accuracy on trial {i}: {accuracy}")

        # --- sum over trials ---
        summed_tps = summed_tps_condition_b if b_trial else summed_tps_condition_a
        summed_bigrams = summed_bigrams_condition_b if b_trial else summed_bigrams_condition_a

        for (a, b), count in bigrams.items():
            if (a, b) not in summed_bigrams:
                summed_bigrams[(a, b)] = 0
            summed_bigrams[(a, b)] += count

        for (a, b), probability in tps.items():
            if (a, b) not in summed_tps:
                summed_tps[(a, b)] = 0
            summed_tps[(a, b)] += probability

        summed_accuracy += accuracy

        if b_trial:
            num_trials_b += 1
        else:
            num_trials_a += 1
    average_bigram_count_a = {}
    average_bigram_count_b = {}
    average_tps_a = {}
    average_tps_b = {}

    for (a, b), count in summed_bigrams_condition_a.items():
        average_bigram_count_a[(a, b)] = count / num_trials_a
    for (a, b), count in summed_bigrams_condition_b.items():
        average_bigram_count_b[(a, b)] = count / num_trials_b

    for (a, b), probability in summed_tps_condition_a.items():
        average_tps_a[(a, b)] = probability / num_trials_a
    for (a, b), probability in summed_tps_condition_b.items():
        average_tps_b[(a, b)] = probability / num_trials_b

    average_accuracy = summed_accuracy / num_trials

    return  average_tps_a, average_tps_b, average_bigram_count_a, average_bigram_count_b, average_accuracy


if __name__ == '__main__':
    # experiment to run:
    # Saffran et al.: experiment_nr = 0
    # Aslin et al.: experiment_nr = 1
    experiment_nr = 1
    num_trials = 240

    overall_tps_a, overall_tps_b, bigrams_a, bigrams_b, overall_accuracy = run_experiment(experiment_nr, num_trials)
    print(f"overall_accuracy on 24 trials: {overall_accuracy}")
    print(f"overall_tps on 24 trials: {overall_tps_a, overall_tps_b}")
    plot_results(overall_tps_a, overall_tps_b, bigrams_a, bigrams_b, experiment_nr)