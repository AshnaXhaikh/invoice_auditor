# --- utils/benford_check.py ---
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def run_benford_analysis(data):
    if isinstance(data, str):
        numbers = list(map(float, re.findall(r"\\b\\d+(?:\\.\\d+)?\\b", data)))
    else:
        numbers = pd.to_numeric(data.select_dtypes(include=["number"]).stack(), errors='coerce').dropna().values

    first_digits = [int(str(abs(num))[0]) for num in numbers if str(abs(num))[0].isdigit() and num != 0]
    observed = Counter(first_digits)

    total = sum(observed.values())
    observed_freq = [observed.get(d, 0)/total for d in range(1,10)]
    expected_freq = [np.log10(1 + 1/d) for d in range(1,10)]

    fig, ax = plt.subplots()
    ax.bar(range(1,10), observed_freq, label="Observed", alpha=0.7)
    ax.plot(range(1,10), expected_freq, label="Expected", color="red", marker="o")
    ax.set_title("Benford's Law Distribution")
    ax.set_xlabel("Leading Digit")
    ax.set_ylabel("Frequency")
    ax.legend()

    summary = {"observed": observed_freq, "expected": expected_freq}
    return summary, fig
