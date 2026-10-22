#!/usr/bin/env python3
"""
Generate README.md and weekly distribution graphs from parquet data.

Usage:
    python docs/generate_readme_and_graphs.py \
        --perf PATH_TO_PERFORMANCE_PARQUET \
        --intel PATH_TO_INTELLIGENCE_PARQUET \
        --readme README.md

If parquet paths are omitted the script will look for files matching
`*performance*.parquet` and `*intelligence*.parquet` in the repository root.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def find_parquet(root: Path, pattern: str) -> Path | None:
    files = list(root.glob(pattern))
    return files[0] if files else None


def parse_date_column(s: pd.Series) -> pd.Series:
    # Example: '2026-09-15 05:08:18 (GMT)'
    # Remove any parenthetical timezone suffix and parse
    cleaned = s.fillna("").astype(str).str.replace(r"\s*\(.*\)$", "", regex=True)
    return pd.to_datetime(cleaned, errors="coerce")


def weekly_counts_from_datecol(df: pd.DataFrame, col: str) -> pd.Series:
    dt = parse_date_column(df[col])
    dt = dt.dropna()
    if dt.empty:
        return pd.Series(dtype=int)
    # Use weekly bins starting on Monday for readability
    series = dt.dt.to_period("W").apply(lambda p: p.start_time)
    counts = series.value_counts().sort_index()
    counts.index = pd.to_datetime(counts.index)
    return counts


def plot_weekly(counts: pd.Series, out_png: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 4))
    if counts.empty:
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
    else:
        ax.bar(counts.index, counts.values, width=6)
        ax.set_xlim(counts.index.min() - pd.Timedelta(days=2), counts.index.max() + pd.Timedelta(days=9))
        ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator())
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y-%m-%d"))
        fig.autofmt_xdate()
    ax.set_title(title)
    ax.set_ylabel("Rows per week")
    plt.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150)
    plt.close(fig)


def make_columns_table(df: pd.DataFrame) -> str:
    rows = []
    for i, col in enumerate(df.columns):
        nonnull = int(df[col].notna().sum())
        dtype = str(df[col].dtype)
        rows.append(f"| {i} | {col} | {nonnull} non-null | {dtype} |")
    header = "|  # | Column | Non-Null Count | Dtype  |\n| -: | ----------------- | --------------: | :----- |"
    return header + "\n" + "\n".join(rows)


def generate_readme(
    perf_df: pd.DataFrame,
    intel_df: pd.DataFrame,
    template_path: Path,
    readme_path: Path,
) -> None:
    template = template_path.read_text(encoding="utf8")
    replacements = {
        "{{PERFORMANCE_ROWS}}": f"{len(perf_df):,}",
        "{{PERFORMANCE_COLUMNS}}": str(len(perf_df.columns)),
        "{{PERFORMANCE_SCHEMA}}": make_columns_table(perf_df),
        "{{INTELLIGENCE_ROWS}}": f"{len(intel_df):,}",
        "{{INTELLIGENCE_COLUMNS}}": str(len(intel_df.columns)),
        "{{INTELLIGENCE_SCHEMA}}": make_columns_table(intel_df),
    }
    for placeholder, value in replacements.items():
        if placeholder not in template:
            raise ValueError(f"Template is missing required placeholder: {placeholder}")
        template = template.replace(placeholder, value)

    readme_path.write_text(template, encoding="utf8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--perf", type=Path, help="performance parquet file")
    p.add_argument("--intel", type=Path, help="intelligence parquet file")
    p.add_argument("--template", type=Path, default=Path("docs/README.template.md"))
    p.add_argument("--readme", type=Path, default=Path("README.md"))
    p.add_argument("--docs-dir", type=Path, default=Path("docs"))
    args = p.parse_args(argv)

    repo_root = Path.cwd()

    perf_path = args.perf or find_parquet(repo_root, "*performance*.parquet")
    intel_path = args.intel or find_parquet(repo_root, "*intelligence*.parquet")

    if perf_path is None:
        print("Performance parquet not found. Provide with --perf." , file=sys.stderr)
        return 2
    if intel_path is None:
        print("Intelligence parquet not found. Provide with --intel." , file=sys.stderr)
        return 2

    print(f"Reading performance data from: {perf_path}")
    perf_df = pd.read_parquet(perf_path)
    print(f"Reading intelligence data from: {intel_path}")
    intel_df = pd.read_parquet(intel_path)

    # Generate weekly distribution PNGs
    perf_counts = weekly_counts_from_datecol(perf_df, "date_data_tip")
    intel_counts = weekly_counts_from_datecol(intel_df, "date_data_tip")

    perf_png = args.docs_dir / "distribution_performance.png"
    intel_png = args.docs_dir / "distribution_intelligence.png"
    plot_weekly(perf_counts, perf_png, "Weekly distribution of performance data")
    plot_weekly(intel_counts, intel_png, "Weekly distribution of intelligence data")

    # Update README.md
    generate_readme(perf_df, intel_df, args.template, args.readme)

    print("Done. Generated graphs in", str(args.docs_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
