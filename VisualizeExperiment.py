import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
from DataPreparation import *

def plot_results(tps_a: dict, tps_b: dict, bigrams_a: dict, bigrams_b: dict, experiment_nr):

    condition_a, condition_b, _ = pick_training_set_from_expnr(experiment_nr)

    def get_within_between_pairs(tps: dict, condition: list[str]) -> tuple[dict, dict]:
        """split TP dict into within-word and between-word pairs"""
        within = {}
        between = {}
        # collect all within-word pairs for this condition
        within_pairs = set()
        for word in condition:
            syllables = syllabify(word)
            for i in range(len(syllables) - 1):
                within_pairs.add((syllables[i], syllables[i+1]))

        for pair, tp in tps.items():
            if pair in within_pairs:
                within[pair] = tp
            else:
                between[pair] = tp
        return within, between

    within_a, between_a = get_within_between_pairs(tps_a, condition_a)
    within_b, between_b = get_within_between_pairs(tps_b, condition_b)

    def make_legend(mean_val):
        return [
            mlines.Line2D([0], [0], color="steelblue", linewidth=6, label="within-word"),
            mlines.Line2D([0], [0], color="salmon",    linewidth=6, label="between-word"),
            mlines.Line2D([0], [0], color="dimgray", linestyle="--", label=f"mean = {mean_val:.2f}"),
        ]

    # --- Plot 1: TPs ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 9))

    def plot_all_pairs(ax, within, between, title):
        within_sorted = dict(sorted(within.items(), key=lambda x: x[1], reverse=True))
        between_sorted = dict(sorted(between.items(), key=lambda x: x[1], reverse=True))

        pairs = list(within_sorted.keys()) + list(between_sorted.keys())
        values = list(within_sorted.values()) + list(between_sorted.values())
        colors = ["steelblue"] * len(within_sorted) + ["salmon"] * len(between_sorted)
        x = np.arange(len(pairs))
        labels = [f"{a}-{b}" for a, b in pairs]

        ax.bar(x, values, color=colors)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=16)
        ax.set_title(title, fontsize=16)
        ax.set_ylabel("Mean TP", fontsize = 16)
        ax.set_ylim(0, 1.1)
        ax.tick_params(axis='y', labelsize=16)
        mean_val = np.mean(values)
        ax.axhline(y=mean_val, color="dimgray", linestyle="--", linewidth=1)
        ax.legend(handles=make_legend(mean_val), loc="upper right", fontsize=16)

    plot_all_pairs(ax1, within_a, between_a, "Condition A")
    plot_all_pairs(ax2, within_b, between_b, "Condition B")

    plt.tight_layout()
    plt.show()

    # --- Plot 2: Bigram frequencies ---
    fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(9, 9), sharey=True)

    def plot_bigram_frequencies(ax, bigrams, within, between, title):
        within_sorted = dict(
            sorted({p: bigrams[p] for p in within if p in bigrams}.items(), key=lambda x: x[1], reverse=True))
        between_sorted = dict(
            sorted({p: bigrams[p] for p in between if p in bigrams}.items(), key=lambda x: x[1], reverse=True))

        pairs = list(within_sorted.keys()) + list(between_sorted.keys())
        values = list(within_sorted.values()) + list(between_sorted.values())
        colors = ["steelblue"] * len(within_sorted) + ["salmon"] * len(between_sorted)
        x = np.arange(len(pairs))
        labels = [f"{a}-{b}" for a, b in pairs]

        ax.bar(x, values, color=colors)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=16)
        ax.set_ylabel("Bigram frequency", fontsize = 16)
        ax.set_title(title, fontsize=16)
        ax.tick_params(axis='y', labelsize=16)
        mean_val = np.mean(values)
        ax.axhline(y=mean_val, color="dimgray", linestyle="--", linewidth=1)
        ax.legend(handles=make_legend(mean_val), loc="upper right", fontsize=16)

    plot_bigram_frequencies(ax3, bigrams_a, within_a, between_a, "Condition A")
    plot_bigram_frequencies(ax4, bigrams_b, within_b, between_b, "Condition B")

    plt.tight_layout()
    plt.show()