import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error


def gini(y_true, y_pred, sample_weight=None):
    """
    sklearn-type gini

    y_truearray-like of shape (n_samples,) or (n_samples, n_outputs)
    Ground truth (correct) target values.

    y_predarray-like of shape (n_samples,) or (n_samples, n_outputs)
    Estimated target values.

    sample_weightarray-like of shape (n_samples,), default=None
    Sample weights.

    returns metric value as float

    source: https://stackoverflow.com/questions/48999542/more-efficient-weighted-gini-coefficient-in-python
    """

    # The rest of the code requires numpy arrays.
    y_true = np.asarray(y_true)
    if sample_weight is not None:
        sample_weight = np.asarray(sample_weight)
        sorted_indices = np.argsort(y_pred)
        sorted_x = y_true[sorted_indices]
        sorted_w = sample_weight[sorted_indices]
        # Force float dtype to avoid overflows
        cumw = np.cumsum(sorted_w, dtype=float)
        cumxw = np.cumsum(sorted_x * sorted_w, dtype=float)

        min_weight = min(sample_weight)
        total_weight = sum(sample_weight)
        adjustment_factor = total_weight / (total_weight - min_weight)

        return (
            np.sum(cumxw[1:] * cumw[:-1] - cumxw[:-1] * cumw[1:])
            / (cumxw[-1] * cumw[-1])
        ) * adjustment_factor
    else:
        sorted_indices = np.argsort(y_pred)
        sorted_x = y_true[sorted_indices]
        n = len(y_true)
        cumx = np.cumsum(sorted_x, dtype=float)
        # The above formula, with all weights equal to 1 simplifies to:
        adjustment_factor = n / (n - 1)  # for bias
        return (n + 1 - 2 * np.sum(cumx) / cumx[-1]) / n * adjustment_factor


def group_data(y_true, y_pred, sample_weight=None, split=5) -> pd.DataFrame:
    """group validation metrics into specified splits

    Args:
        y_true (array-like): _description_
        y_pred (array-like): _description_
        sample_weight (array-like, optional): _description_. Defaults to None.
        split (int, optional): _description_. Defaults to 5.

    Returns:
        pd.DataFrame: dataframe with first three inputs as columns, summing weights and
        grouping in order of predicted weights

    References:
        https://en.wikipedia.org/wiki/Hosmer%E2%80%93Lemeshow_test
    """

    if sample_weight == None:
        sample_weight = np.ones(len(y_true))

    sample_weight = np.asarray(sample_weight)
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    sorted_indices = np.argsort(y_pred)

    sorted_df = pd.DataFrame(
        {
            "y_true": y_true[sorted_indices],
            "y_pred": y_pred[sorted_indices],
            "sample_weight": sample_weight[sorted_indices],
        }
    )

    # mapping of rows to bins
    out = pd.qcut(sorted_df["y_pred"], split, duplicates="drop")

    sorted_df["pred_group"] = out

    grouped_df = (
        sorted_df.groupby("pred_group")
        .mean()[["y_true", "y_pred"]]
        .join(sorted_df.groupby("pred_group").sum()[["sample_weight"]])
    )

    return grouped_df


def ginierror(y_true, y_pred, sample_weight=None, split=5, plot=True):
    """gini minus mae of grouped data

    Args:
        y_true (_type_): _description_
        y_pred (_type_): _description_
        sample_weight (_type_, optional): _description_. Defaults to None.
        split (int, optional): _description_. Defaults to 5.
        plot (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    grouped_df = group_data(y_true, y_pred, sample_weight, split)

    gini_result = gini(
        grouped_df["y_true"],
        grouped_df["y_pred"],
        sample_weight=grouped_df["sample_weight"],
    )

    mae_result = mean_absolute_error(
        grouped_df["y_true"],
        grouped_df["y_pred"],
        sample_weight=grouped_df["sample_weight"],
    )

    if plot:
        fig, ax = plt.subplots()
        ax2 = ax.twinx()

        grouped_df[["y_true", "y_pred"]].plot(linestyle="-", marker="o", ax=ax)
        grouped_df["sample_weight"].plot(kind="bar", ax=ax2, alpha=0.25)

        plt.show()

    return gini_result - mae_result
