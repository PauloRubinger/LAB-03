"""
Script 3: Statistical analysis and visualization of collected data.

Answers the 8 research questions (RQ01-RQ08) using:
- Descriptive statistics (median, mean, standard deviation)
- Spearman correlation (non-parametric data)
- Boxplots and scatter plots
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data/processed", "pull_requests.csv")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "figures")

os.makedirs(FIGURES_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
})
DPI = 200
SOURCE_NOTE = "Fonte: GitHub GraphQL API v4 — Top-200 repositórios por stars (mai/2026)"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE)
    df["total_lines"] = df["additions"] + df["deletions"]
    print(f"Dataset loaded: {len(df)} PRs")
    print(f"  MERGED: {(df['state'] == 'MERGED').sum()}")
    print(f"  CLOSED: {(df['state'] == 'CLOSED').sum()}")
    return df


def spearman_test(x, y, label_x, label_y, rq=None, results=None):
    """Calculate Spearman correlation and return formatted result."""
    corr, pvalue = stats.spearmanr(x, y, nan_policy="omit")
    sig = "Yes" if pvalue < 0.05 else "No"
    print(f"  Spearman({label_x} x {label_y}): rho={corr:.4f}, p={pvalue:.2e}, Significant={sig}")
    if results is not None:
        results.append({
            "RQ": rq,
            "Test": "Spearman",
            "Variable_X": label_x,
            "Variable_Y": label_y,
            "Statistic": round(corr, 4),
            "P_value": pvalue,
            "Significant": sig,
        })
    return corr, pvalue


def descriptive_stats(df, column, group_col="state"):
    """Display descriptive statistics per group."""
    print(f"\n  Statistics of '{column}' by {group_col}:")
    grouped = df.groupby(group_col)[column].describe()
    print(grouped.to_string())

    medians = df.groupby(group_col)[column].median()
    print(f"  Medians: {medians.to_dict()}")
    return medians


def mannwhitney_test(group1, group2, metric, rq, results):
    """Run Mann-Whitney U test and record result."""
    stat, p = stats.mannwhitneyu(group1, group2, alternative="two-sided")
    sig = "Yes" if p < 0.05 else "No"
    print(f"  Mann-Whitney U ({metric}): U={stat:.0f}, p={p:.2e}")
    results.append({
        "RQ": rq,
        "Test": "Mann-Whitney U",
        "Variable_X": metric,
        "Variable_Y": "state (MERGED vs CLOSED)",
        "Statistic": round(stat, 0),
        "P_value": p,
        "Significant": sig,
    })
    return stat, p


# ============================================================
# Dimension A: Final Review Feedback (Status MERGED vs CLOSED)
# ============================================================

def rq01(df, results):
    """RQ01: PR size vs final review feedback."""
    print("\n" + "=" * 60)
    print("RQ01: PR Size vs Final Review Feedback")
    print("=" * 60)

    for metric in ["changed_files", "additions", "deletions", "total_lines"]:
        descriptive_stats(df, metric)

    # Boxplot
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    for ax, col, title, ylabel in zip(axes,
                               ["changed_files", "additions", "deletions"],
                               ["Arquivos Alterados", "Linhas Adicionadas", "Linhas Removidas"],
                               ["Arquivos Alterados", "Linhas Adicionadas", "Linhas Removidas"]):
        sns.boxplot(data=df, x="state", y=col, order=["MERGED", "CLOSED"], ax=ax, showfliers=False)
        ax.set_title(title)
        ax.set_xlabel("Status do PR")
        ax.set_ylabel(ylabel)
    fig.suptitle("RQ01 — Tamanho dos PRs por Status", fontsize=15, fontweight="bold", y=1.01)
    fig.text(0.5, -0.02, SOURCE_NOTE, ha="center", fontsize=10, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq01_tamanho_vs_status.png"), dpi=DPI, bbox_inches="tight")
    plt.close()

    # Mann-Whitney U test (compare MERGED vs CLOSED)
    for metric in ["changed_files", "additions", "deletions"]:
        merged = df[df["state"] == "MERGED"][metric].dropna()
        closed = df[df["state"] == "CLOSED"][metric].dropna()
        mannwhitney_test(merged, closed, metric, "RQ01", results)


def rq02(df, results):
    """RQ02: Analysis time vs final review feedback."""
    print("\n" + "=" * 60)
    print("RQ02: Analysis Time vs Final Review Feedback")
    print("=" * 60)

    descriptive_stats(df, "analysis_time_hours")

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(data=df, x="state", y="analysis_time_hours", order=["MERGED", "CLOSED"], ax=ax, showfliers=False)
    ax.set_title("RQ02 — Tempo de Análise por Status do PR", fontweight="bold")
    ax.set_ylabel("Tempo de Análise (horas)")
    ax.set_xlabel("Status do PR")
    fig.text(0.5, -0.02, SOURCE_NOTE, ha="center", fontsize=10, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq02_tempo_vs_status.png"), dpi=DPI, bbox_inches="tight")
    plt.close()

    merged = df[df["state"] == "MERGED"]["analysis_time_hours"].dropna()
    closed = df[df["state"] == "CLOSED"]["analysis_time_hours"].dropna()
    mannwhitney_test(merged, closed, "analysis_time_hours", "RQ02", results)


def rq03(df, results):
    """RQ03: PR description vs final review feedback."""
    print("\n" + "=" * 60)
    print("RQ03: PR Description vs Final Review Feedback")
    print("=" * 60)

    descriptive_stats(df, "body_length")

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(data=df, x="state", y="body_length", order=["MERGED", "CLOSED"], ax=ax, showfliers=False)
    ax.set_title("RQ03 — Descrição dos PRs por Status", fontweight="bold")
    ax.set_ylabel("Caracteres do Body")
    ax.set_xlabel("Status do PR")
    fig.text(0.5, -0.02, SOURCE_NOTE, ha="center", fontsize=10, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq03_descricao_vs_status.png"), dpi=DPI, bbox_inches="tight")
    plt.close()

    merged = df[df["state"] == "MERGED"]["body_length"].dropna()
    closed = df[df["state"] == "CLOSED"]["body_length"].dropna()
    mannwhitney_test(merged, closed, "body_length", "RQ03", results)


def rq04(df, results):
    """RQ04: PR interactions vs final review feedback."""
    print("\n" + "=" * 60)
    print("RQ04: Interactions vs Final Review Feedback")
    print("=" * 60)

    for metric in ["participants", "comments"]:
        descriptive_stats(df, metric)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    for ax, col, title, ylabel in zip(axes,
                               ["participants", "comments"],
                               ["Nº de Participantes", "Nº de Comentários"],
                               ["Nº de Participantes", "Nº de Comentários"]):
        sns.boxplot(data=df, x="state", y=col, order=["MERGED", "CLOSED"], ax=ax, showfliers=False)
        ax.set_title(f"{title} por Status do PR", fontweight="bold")
        ax.set_xlabel("Status do PR")
        ax.set_ylabel(ylabel)
    fig.suptitle("RQ04 — Interações por Status do PR", fontsize=15, fontweight="bold", y=1.01)
    fig.text(0.5, -0.02, SOURCE_NOTE, ha="center", fontsize=10, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq04_interacoes_vs_status.png"), dpi=DPI, bbox_inches="tight")
    plt.close()

    for metric in ["participants", "comments"]:
        merged = df[df["state"] == "MERGED"][metric].dropna()
        closed = df[df["state"] == "CLOSED"][metric].dropna()
        mannwhitney_test(merged, closed, metric, "RQ04", results)


# ============================================================
# Dimension B: Number of Reviews
# ============================================================

def rq05(df, results):
    """RQ05: PR size vs number of reviews."""
    print("\n" + "=" * 60)
    print("RQ05: PR Size vs Number of Reviews")
    print("=" * 60)

    for metric in ["changed_files", "total_lines", "additions", "deletions"]:
        spearman_test(df[metric], df["review_count"], metric, "review_count", rq="RQ05", results=results)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].scatter(df["changed_files"], df["review_count"], alpha=0.3, s=25)
    _v0 = df[["changed_files", "review_count"]].dropna()
    _s0, _i0, *_ = stats.linregress(_v0["changed_files"], _v0["review_count"])
    _x0 = np.array([_v0["changed_files"].min(), _v0["changed_files"].max()])
    axes[0].plot(_x0, _s0 * _x0 + _i0, color="crimson", linewidth=2, linestyle="--", label="Tendência")
    axes[0].legend(fontsize=10)
    axes[0].set_xlabel("Arquivos Alterados")
    axes[0].set_ylabel("Nº de Revisões")
    axes[0].set_title("Arquivos vs. Revisões", fontweight="bold")

    axes[1].scatter(df["total_lines"], df["review_count"], alpha=0.3, s=25)
    _v1 = df[["total_lines", "review_count"]].dropna()
    _s1, _i1, *_ = stats.linregress(_v1["total_lines"], _v1["review_count"])
    _x1 = np.array([_v1["total_lines"].min(), _v1["total_lines"].max()])
    axes[1].plot(_x1, _s1 * _x1 + _i1, color="crimson", linewidth=2, linestyle="--", label="Tendência")
    axes[1].legend(fontsize=10)
    axes[1].set_xlabel("Total de Linhas (adições + deleções)")
    axes[1].set_ylabel("Nº de Revisões")
    axes[1].set_title("Linhas vs. Revisões", fontweight="bold")
    fig.suptitle("RQ05 — Tamanho dos PRs vs. Número de Revisões", fontsize=15, fontweight="bold", y=1.01)
    fig.text(0.5, -0.02, SOURCE_NOTE, ha="center", fontsize=10, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq05_tamanho_vs_revisoes.png"), dpi=DPI, bbox_inches="tight")
    plt.close()


def rq06(df, results):
    """RQ06: Analysis time vs number of reviews."""
    print("\n" + "=" * 60)
    print("RQ06: Analysis Time vs Number of Reviews")
    print("=" * 60)

    spearman_test(df["analysis_time_hours"], df["review_count"],
                  "analysis_time_hours", "review_count", rq="RQ06", results=results)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df["analysis_time_hours"], df["review_count"], alpha=0.3, s=25)
    _v = df[["analysis_time_hours", "review_count"]].dropna()
    _s, _i, *_ = stats.linregress(_v["analysis_time_hours"], _v["review_count"])
    _x = np.array([_v["analysis_time_hours"].min(), _v["analysis_time_hours"].max()])
    ax.plot(_x, _s * _x + _i, color="crimson", linewidth=2, linestyle="--", label="Tendência")
    ax.legend(fontsize=10)
    ax.set_xlabel("Tempo de Análise (horas)")
    ax.set_ylabel("Nº de Revisões")
    ax.set_title("RQ06 — Tempo de Análise vs. Número de Revisões", fontweight="bold")
    fig.text(0.5, -0.02, SOURCE_NOTE, ha="center", fontsize=10, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq06_tempo_vs_revisoes.png"), dpi=DPI, bbox_inches="tight")
    plt.close()


def rq07(df, results):
    """RQ07: PR description vs number of reviews."""
    print("\n" + "=" * 60)
    print("RQ07: PR Description vs Number of Reviews")
    print("=" * 60)

    spearman_test(df["body_length"], df["review_count"],
                  "body_length", "review_count", rq="RQ07", results=results)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df["body_length"], df["review_count"], alpha=0.3, s=25)
    _v = df[["body_length", "review_count"]].dropna()
    _s, _i, *_ = stats.linregress(_v["body_length"], _v["review_count"])
    _x = np.array([_v["body_length"].min(), _v["body_length"].max()])
    ax.plot(_x, _s * _x + _i, color="crimson", linewidth=2, linestyle="--", label="Tendência")
    ax.legend(fontsize=10)
    ax.set_xlabel("Descrição do PR (caracteres)")
    ax.set_ylabel("Nº de Revisões")
    ax.set_title("RQ07 — Descrição vs. Número de Revisões", fontweight="bold")
    fig.text(0.5, -0.02, SOURCE_NOTE, ha="center", fontsize=10, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq07_descricao_vs_revisoes.png"), dpi=DPI, bbox_inches="tight")
    plt.close()


def rq08(df, results):
    """RQ08: PR interactions vs number of reviews."""
    print("\n" + "=" * 60)
    print("RQ08: Interactions vs Number of Reviews")
    print("=" * 60)

    for metric in ["participants", "comments"]:
        spearman_test(df[metric], df["review_count"], metric, "review_count", rq="RQ08", results=results)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].scatter(df["participants"], df["review_count"], alpha=0.3, s=25)
    _v0 = df[["participants", "review_count"]].dropna()
    _s0, _i0, *_ = stats.linregress(_v0["participants"], _v0["review_count"])
    _x0 = np.array([_v0["participants"].min(), _v0["participants"].max()])
    axes[0].plot(_x0, _s0 * _x0 + _i0, color="crimson", linewidth=2, linestyle="--", label="Tendência")
    axes[0].legend(fontsize=10)
    axes[0].set_xlabel("Nº de Participantes")
    axes[0].set_ylabel("Nº de Revisões")
    axes[0].set_title("Participantes vs. Revisões", fontweight="bold")

    axes[1].scatter(df["comments"], df["review_count"], alpha=0.3, s=25)
    _v1 = df[["comments", "review_count"]].dropna()
    _s1, _i1, *_ = stats.linregress(_v1["comments"], _v1["review_count"])
    _x1 = np.array([_v1["comments"].min(), _v1["comments"].max()])
    axes[1].plot(_x1, _s1 * _x1 + _i1, color="crimson", linewidth=2, linestyle="--", label="Tendência")
    axes[1].legend(fontsize=10)
    axes[1].set_xlabel("Nº de Comentários")
    axes[1].set_ylabel("Nº de Revisões")
    axes[1].set_title("Comentários vs. Revisões", fontweight="bold")
    fig.suptitle("RQ08 — Interações vs. Número de Revisões", fontsize=15, fontweight="bold", y=1.01)
    fig.text(0.5, -0.02, SOURCE_NOTE, ha="center", fontsize=10, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "rq08_interacoes_vs_revisoes.png"), dpi=DPI, bbox_inches="tight")
    plt.close()


def spearman_correlation_matrix(df):
    """Generate and save Spearman correlation matrix for all metrics."""
    print("\n" + "=" * 60)
    print("SPEARMAN CORRELATION MATRIX")
    print("=" * 60)

    metrics = [
        "changed_files", "additions", "deletions", "total_lines",
        "analysis_time_hours", "body_length",
        "participants", "comments", "review_count",
    ]

    corr_matrix = df[metrics].corr(method="spearman")
    print(corr_matrix.to_string())

    # Save as CSV
    corr_path = os.path.join(os.path.dirname(FIGURES_DIR), "spearman_correlation_matrix.csv")
    corr_matrix.to_csv(corr_path, index_label="Metric")

    # Save as heatmap
    fig, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        vmin=-1,
        vmax=1,
        ax=ax,
        linewidths=0.5,
        annot_kws={"size": 11},
    )
    ax.set_title("Matriz de Correlação de Spearman", fontsize=15, fontweight="bold", pad=12)
    fig.text(0.5, -0.01, SOURCE_NOTE, ha="center", fontsize=10, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "spearman_correlation_matrix.png"), dpi=DPI, bbox_inches="tight")
    plt.close()

    print(f"Correlation matrix saved to: {corr_path}")
    return corr_matrix


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
    summary.to_csv(os.path.join(os.path.dirname(FIGURES_DIR), "summary_stats.csv"), index_label="Metric")


def main():
    df = load_data()
    results = []

    # Dimension A
    rq01(df, results)
    rq02(df, results)
    rq03(df, results)
    rq04(df, results)

    # Dimension B
    rq05(df, results)
    rq06(df, results)
    rq07(df, results)
    rq08(df, results)

    # Summary table
    summary_table(df)

    # Spearman correlation matrix
    spearman_correlation_matrix(df)

    # Save all statistical test results
    results_path = os.path.join(os.path.dirname(FIGURES_DIR), "statistical_tests.csv")
    pd.DataFrame(results).to_csv(results_path, index=False)
    print(f"Statistical tests saved to: {results_path}")

    print(f"\nFigures saved to: {FIGURES_DIR}")
    print("Analysis completed!")


if __name__ == "__main__":
    main()
