# code/model_prep.py
"""
Prepare modeling matrices for the Opportunity-Adjusted Football Prospect Evaluation project.

Goal:
- Baseline model features (what scouts normally see)
- Constraint-aware features (baseline + opportunity inputs)
- Clean split into X/y for training

Assumptions:
- You run data_ingest.py first and create a processed CSV/parquet.
- Processed dataset contains canonical column names from your schema.
- Numeric mapped columns end with *_num (recommended).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict

import pandas as pd


# ----------------------------
# Feature definitions (V1)
# ----------------------------

# Baseline: performance + context + recognition (NO opportunity inputs)
BASELINE_FEATURES: List[str] = [
    # Categorical mapped -> numeric
    "position_group_num",
    "school_classification_num",
    "competition_level_num",
    "snaps_estimate_num",

    # Numeric / parsed
    "games_played",
    "offseason_participation_weeks",  # you may move this to constraints if you consider it an "opportunity" input

    # Honors
    "honors_level_num",
]

# Constraint inputs: development access + constraints
CONSTRAINT_FEATURES: List[str] = [
    "training_hours_num",
    "coaching_hours_num",
    "weight_room_access_num",
    "film_hours_num",
    "job_hours_num",
    "commute_minutes_num",
    "missed_offseason_num",  # if you created this as numeric; otherwise use missed_offseason_binary
]

# Raw text fields you should keep for later feature engineering, but NOT model directly yet
TEXT_CONTEXT_FIELDS: List[str] = [
    "primary_production_stat",
    "team_record_or_win_pct",
]

# Targets (V1)
TARGETS: Dict[str, str] = {
    "college_roster_binary": "college_roster_binary",
    "college_level": "college_level",
    "year1_snaps_bucket": "year1_snaps_bucket",
}


@dataclass(frozen=True)
class PrepConfig:
    baseline_features: List[str] = tuple(BASELINE_FEATURES)  # type: ignore
    constraint_features: List[str] = tuple(CONSTRAINT_FEATURES)  # type: ignore
    text_fields: List[str] = tuple(TEXT_CONTEXT_FIELDS)  # type: ignore
    id_col: str = "player_id"
    consent_col: str = "consent_ok"  # produced in ingest; safe to keep filtering here too
    dropna_y: bool = True


# ----------------------------
# Core helpers
# ----------------------------

def load_processed(path: str) -> pd.DataFrame:
    """
    Load processed dataset from CSV or Parquet.
    """
    if path.endswith(".parquet"):
        return pd.read_parquet(path)
    return pd.read_csv(path)


def ensure_columns(df: pd.DataFrame, cols: List[str], *, name: str = "columns") -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required {name}: {missing}")


def coerce_numeric(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """
    Force numeric coercion where possible; keep Int64/float compatibility.
    """
    out = df.copy()
    for c in cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


# ----------------------------
# Public API
# ----------------------------

def prepare_xy(
    df: pd.DataFrame,
    *,
    target: str = "college_roster_binary",
    config: Optional[PrepConfig] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """
    Returns:
      X_base: baseline feature matrix
      X_full: baseline + constraint feature matrix
      y: target series
    """
    cfg = config or PrepConfig()

    if target not in TARGETS:
        raise ValueError(f"Unknown target: {target}. Choose from: {list(TARGETS.keys())}")

    # Optional extra consent filter (ingest should already do this)
    if cfg.consent_col in df.columns:
        df = df[df[cfg.consent_col] == True].copy()  # noqa: E712

    # Define feature sets
    base_cols = list(cfg.baseline_features)
    full_cols = list(cfg.baseline_features) + list(cfg.constraint_features)

    # Validate presence
    ensure_columns(df, base_cols, name="baseline features")
    ensure_columns(df, full_cols, name="full features")
    ensure_columns(df, [TARGETS[target]], name="target")

    # Coerce numeric inputs (safe)
    df = coerce_numeric(df, base_cols + list(cfg.constraint_features))

    # Build matrices
    X_base = df[base_cols].copy()
    X_full = df[full_cols].copy()
    y = df[TARGETS[target]].copy()

    # Optionally drop rows with missing y
    if cfg.dropna_y:
        mask = ~pd.isna(y)
        X_base = X_base.loc[mask].copy()
        X_full = X_full.loc[mask].copy()
        y = y.loc[mask].copy()

    return X_base, X_full, y


def prepare_with_metadata(
    df: pd.DataFrame,
    *,
    target: str = "college_roster_binary",
    config: Optional[PrepConfig] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    Same as prepare_xy, but also returns a metadata frame with IDs + raw text context fields.
    Useful for reporting/explainability later.
    """
    cfg = config or PrepConfig()

    X_base, X_full, y = prepare_xy(df, target=target, config=cfg)

    meta_cols = [c for c in [cfg.id_col] + list(cfg.text_fields) if c in df.columns]
    meta = df.loc[X_base.index, meta_cols].copy() if meta_cols else pd.DataFrame(index=X_base.index)

    return X_base, X_full, y, meta


# ----------------------------
# Minimal CLI (optional)
# ----------------------------

def _cli() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Processed dataset path (.csv or .parquet)")
    ap.add_argument("--target", default="college_roster_binary", help=f"One of: {list(TARGETS.keys())}")
    args = ap.parse_args()

    df = load_processed(args.input)
    Xb, Xf, y = prepare_xy(df, target=args.target)

    print("Rows:", len(y))
    print("Baseline features:", list(Xb.columns))
    print("Full features:", list(Xf.columns))
    print("Target:", args.target)


if __name__ == "__main__":
    _cli()
