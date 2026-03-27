import matplotlib.pyplot as plt
import numpy as np
from DataPreparation import *

def plot_results(tps_a: dict, tps_b: dict):

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

    # --- Plot 1 ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

    def plot_all_pairs(ax, within, between, title):
        # within-word pairs first, then between-word
        pairs = list(within.keys()) + list(between.keys())
        values = list(within.values()) + list(between.values())
        colors = ["steelblue"] * len(within) + ["salmon"] * len(between)
        x = np.arange(len(pairs))
        labels = [f"{a}-{b}" for a, b in pairs]

        ax.bar(x, values, color=colors)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_title(title)
        ax.set_ylabel("Mean TP")
        ax.set_ylim(0, 1.1)
        # divider line between within and between
        ax.axvline(x=len(within) - 0.5, color="gray", linestyle="--", linewidth=1)

    plot_all_pairs(ax1, within_a, between_a, "Condition A – all pairs")
    plot_all_pairs(ax2, within_b, between_b, "Condition B – all pairs")

    from matplotlib.patches import Patch
    legend = [Patch(facecolor="steelblue", label="within-word"),
              Patch(facecolor="salmon",    label="between-word")]
    fig.legend(handles=legend, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.05))
    plt.suptitle("Plot 1: TP per syllable pair")
    plt.tight_layout()
    plt.savefig("plot1_all_pairs.png", dpi=150, bbox_inches="tight")
    plt.show()

    # --- Plot 2 ---
    fig, ax = plt.subplots(figsize=(7, 5))

    avg_within_a = sum(within_a.values())  / len(within_a)
    avg_between_a = sum(between_a.values()) / len(between_a)
    avg_within_b = sum(within_b.values())  / len(within_b)
    avg_between_b = sum(between_b.values()) / len(between_b)

    x = np.arange(2)  # within / between
    width = 0.3

    ax.bar(x - width/2, [avg_within_a, avg_between_a], width, color="steelblue", label="Condition A")
    ax.bar(x + width/2, [avg_within_b, avg_between_b], width, color="salmon",    label="Condition B")

    ax.set_xticks(x)
    ax.set_xticklabels(["within-word pairs", "between-word pairs"])
    ax.set_ylabel("Mean TP")
    ax.set_ylim(0, 1.1)
    ax.set_title("Plot 2: Average TP – within vs. between word boundaries")
    ax.legend()

    plt.tight_layout()
    plt.savefig("plot2_averaged.png", dpi=150, bbox_inches="tight")
    plt.show()