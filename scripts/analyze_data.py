"""
Script 3: Statistical analysis and visualization of collected data.

Answers the 8 research questions (RQ01-RQ08) using:
- Descriptive statistics (median, mean, standard deviation)
- Spearman correlation (non-parametric data)
- Boxplots and scatter plots
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data/processed", "pull_requests.csv")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "figures")

os.makedirs(FIGURES_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE)
    df["total_lines"] = df["additions"] + df["deletions"]
    print(f"Dataset loaded: {len(df)} PRs")
    print(f"  MERGED: {(df['state'] == 'MERGED').sum()}")
    print(f"  CLOSED: {(df['state'] == 'CLOSED').sum()}")
    return df


def spearman_test(x, y, label_x, label_y):
    """Calculate Spearman correlation and return formatted result."""
    corr, pvalue = stats.spearmanr(x, y, nan_policy="omit")
    sig = "Yes" if pvalue < 0.05 else "No"
    print(f"  Spearman({label_x} x {label_y}): rho={corr:.4f}, p={pvalue:.2e}, Significant={sig}")
    return corr, pvalue


def descriptive_stats(df, column, group_col="state"):
    """Display descriptive statistics per group."""
    print(f"\n  Statistics of '{column}' by {group_col}:")
    grouped = df.groupby(group_col)[column].describe()
    print(grouped.to_string())

    medians = df.groupby(group_col)[column].median()
    print(f"  Medians: {medians.to_dict()}")
    return medians


# ============================================================
# Dimension A: Final Review Feedback (Status MERGED vs CLOSED)
# ============================================================

def rq01(df):
    """RQ01: PR size vs final review feedback."""
    print("\n" + "=" * 60)
    print("RQ01: PR Size vs Final Review Feedback")
    print("=" * 60)

    for metric in ["changed_files", "additions", "deletions", "total_lines"]:
        descriptive_stats(df, metric)

    # Boxplot
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, col, title in zip(axes,
                               ["changed_files", "additions", "deletions"],
                               ["Arquivos Alterados", "Linhas Adicionadas", "Linhas Removidas"]):
        sns.boxplot(data=df, x="state", y=col, ax=ax, showfliers=False)
        ax.set_title(title)
        ax.set_xlabel("Status do PR")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq01_tamanho_vs_status.png"), dpi=150)
    plt.close()

    # Mann-Whitney U test (compare MERGED vs CLOSED)
    for metric in ["changed_files", "total_lines"]:
        merged = df[df["state"] == "MERGED"][metric].dropna()
        closed = df[df["state"] == "CLOSED"][metric].dropna()
        stat, p = stats.mannwhitneyu(merged, closed, alternative="two-sided")
        print(f"  Mann-Whitney U ({metric}): U={stat:.0f}, p={p:.2e}")


def rq02(df):
    """RQ02: Analysis time vs final review feedback."""
    print("\n" + "=" * 60)
    print("RQ02: Analysis Time vs Final Review Feedback")
    print("=" * 60)

    descriptive_stats(df, "analysis_time_hours")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="state", y="analysis_time_hours", ax=ax, showfliers=False)
    ax.set_title("Analysis Time by PR Status")
    ax.set_ylabel("Hours")
    ax.set_xlabel("PR Status")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq02_tempo_vs_status.png"), dpi=150)
    plt.close()

    merged = df[df["state"] == "MERGED"]["analysis_time_hours"].dropna()
    closed = df[df["state"] == "CLOSED"]["analysis_time_hours"].dropna()
    stat, p = stats.mannwhitneyu(merged, closed, alternative="two-sided")
    print(f"  Mann-Whitney U (analysis_time_hours): U={stat:.0f}, p={p:.2e}")


def rq03(df):
    """RQ03: PR description vs final review feedback."""
    print("\n" + "=" * 60)
    print("RQ03: PR Description vs Final Review Feedback")
    print("=" * 60)

    descriptive_stats(df, "body_length")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="state", y="body_length", ax=ax, showfliers=False)
    ax.set_title("Description Size by PR Status")
    ax.set_ylabel("Characters")
    ax.set_xlabel("PR Status")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq03_descricao_vs_status.png"), dpi=150)
    plt.close()

    merged = df[df["state"] == "MERGED"]["body_length"].dropna()
    closed = df[df["state"] == "CLOSED"]["body_length"].dropna()
    stat, p = stats.mannwhitneyu(merged, closed, alternative="two-sided")
    print(f"  Mann-Whitney U (body_length): U={stat:.0f}, p={p:.2e}")


def rq04(df):
    """RQ04: PR interactions vs final review feedback."""
    print("\n" + "=" * 60)
    print("RQ04: Interactions vs Final Review Feedback")
    print("=" * 60)

    for metric in ["participants", "comments"]:
        descriptive_stats(df, metric)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, col, title in zip(axes,
                               ["participants", "comments"],
                               ["Participants", "Comments"]):
        sns.boxplot(data=df, x="state", y=col, ax=ax, showfliers=False)
        ax.set_title(f"{title} by PR Status")
        ax.set_xlabel("PR Status")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq04_interacoes_vs_status.png"), dpi=150)
    plt.close()

    for metric in ["participants", "comments"]:
        merged = df[df["state"] == "MERGED"][metric].dropna()
        closed = df[df["state"] == "CLOSED"][metric].dropna()
        stat, p = stats.mannwhitneyu(merged, closed, alternative="two-sided")
        print(f"  Mann-Whitney U ({metric}): U={stat:.0f}, p={p:.2e}")


# ============================================================
# Dimension B: Number of Reviews
# ============================================================

def rq05(df):
    """RQ05: PR size vs number of reviews."""
    print("\n" + "=" * 60)
    print("RQ05: PR Size vs Number of Reviews")
    print("=" * 60)

    for metric in ["changed_files", "total_lines", "additions", "deletions"]:
        spearman_test(df[metric], df["review_count"], metric, "review_count")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(df["changed_files"], df["review_count"], alpha=0.3, s=10)
    axes[0].set_xlabel("Changed Files")
    axes[0].set_ylabel("Number of Reviews")
    axes[0].set_title("Files vs Reviews")

    axes[1].scatter(df["total_lines"], df["review_count"], alpha=0.3, s=10)
    axes[1].set_xlabel("Total Lines (add + del)")
    axes[1].set_ylabel("Number of Reviews")
    axes[1].set_title("Lines vs Reviews")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq05_tamanho_vs_revisoes.png"), dpi=150)
    plt.close()


def rq06(df):
    """RQ06: Analysis time vs number of reviews."""
    print("\n" + "=" * 60)
    print("RQ06: Analysis Time vs Number of Reviews")
    print("=" * 60)

    spearman_test(df["analysis_time_hours"], df["review_count"],
                  "analysis_time_hours", "review_count")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["analysis_time_hours"], df["review_count"], alpha=0.3, s=10)
    ax.set_xlabel("Analysis Time (hours)")
    ax.set_ylabel("Number of Reviews")
    ax.set_title("Analysis Time vs Reviews")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq06_tempo_vs_revisoes.png"), dpi=150)
    plt.close()


def rq07(df):
    """RQ07: PR description vs number of reviews."""
    print("\n" + "=" * 60)
    print("RQ07: PR Description vs Number of Reviews")
    print("=" * 60)

    spearman_test(df["body_length"], df["review_count"],
                  "body_length", "review_count")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["body_length"], df["review_count"], alpha=0.3, s=10)
    ax.set_xlabel("Description Size (characters)")
    ax.set_ylabel("Number of Reviews")
    ax.set_title("Description vs Reviews")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq07_descricao_vs_revisoes.png"), dpi=150)
    plt.close()


def rq08(df):
    """RQ08: PR interactions vs number of reviews."""
    print("\n" + "=" * 60)
    print("RQ08: Interactions vs Number of Reviews")
    print("=" * 60)

    for metric in ["participants", "comments"]:
        spearman_test(df[metric], df["review_count"], metric, "review_count")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(df["participants"], df["review_count"], alpha=0.3, s=10)
    axes[0].set_xlabel("Participants")
    axes[0].set_ylabel("Number of Reviews")
    axes[0].set_title("Participants vs Reviews")

    axes[1].scatter(df["comments"], df["review_count"], alpha=0.3, s=10)
    axes[1].set_xlabel("Comments")
    axes[1].set_ylabel("Number of Reviews")
    axes[1].set_title("Comments vs Reviews")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq08_interacoes_vs_revisoes.png"), dpi=150)
    plt.close()


def summary_table(df):
    """Generate summary table with overall medians."""
    print("\n" + "=" * 60)
    print("SUMMARY TABLE – Overall Medians")
    print("=" * 60)

    metrics = [
        "changed_files", "additions", "deletions", "total_lines",
        "analysis_time_hours", "body_length",
        "participants", "comments", "review_count",
    ]

    summary = df[metrics].median().to_frame("Median")
    summary["Mean"] = df[metrics].mean()
    summary["Std Dev"] = df[metrics].std()
    print(summary.to_string())

    # Save as CSV
    summary.to_csv(os.path.join(os.path.dirname(FIGURES_DIR), "summary_stats.csv"))


def main():
    df = load_data()

    # Dimension A
    rq01(df)
    rq02(df)
    rq03(df)
    rq04(df)

    # Dimension B
    rq05(df)
    rq06(df)
    rq07(df)
    rq08(df)

    # Summary table
    summary_table(df)

    print(f"\nFigures saved to: {FIGURES_DIR}")
    print("Analysis completed!")


if __name__ == "__main__":
    main()
