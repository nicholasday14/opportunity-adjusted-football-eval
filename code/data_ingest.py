# code/data_ingest.py

import argparse
import os
import uuid
import pandas as pd

REQUIRED_COLUMNS = [
    "position_group",
    "games_played",
    "snaps_estimate",
    "primary_production_stat",
    "honors_level",
    "school_classification",
    "competition_level",
    "team_record_or_win_pct",
    "training_hours_per_week",
    "coaching_hours_per_week",
    "weight_room_access_days",
    "film_hours_per_week",
    "offseason_participation_weeks",
    "job_hours_per_week",
    "commute_minutes",
    "missed_offseason_binary",
    "consent_acknowledged"
]

def consent_to_bool(x):
    if x is None:
        return False
    s = str(x).strip().lower()
    return ("agree" in s) or (s in {"yes", "true", "1"})

RENAME_MAP = {
    "Primary Position": "position_group",
    "How many games did you play this season?": "games_played",
    "Total snaps played this season": "snaps_estimate",
    "Enter your main stat (e.g., rushing yards, tackles, pressures). Include the stat name.": "primary_production_stat",
    "Highest honors received this season (if any)": "honors_level",
    "Approximate school enrollment": "school_classification",
    "Level of competition faced - Based on league strength and level of opponents.": "competition_level",
    "Team Record or Win percentage-Example: 8–3 or 72%": "team_record_or_win_pct",
    "Training hours per week (outside of games)": "training_hours_per_week",
    "Coaching or position-specific instructions hours per week": "coaching_hours_per_week",
    "Weight room access per week": "weight_room_access_days",
    "Film study hours per week": "film_hours_per_week",
    "Number of weeks you participated in structured offseason training": "offseason_participation_weeks",
    "Job hours per week during the season": "job_hours_per_week",
    "Approximate daily commute time to practices or training": "commute_minutes",
    "Did you miss 4 or more consecutive offseason weeks for non-injury reasons": "missed_offseason_binary",
    "Consent to Participate": "consent_acknowledged"
}


from code.bin_mapping import (
    map_cat,
    POSITION_GROUP, SCHOOL_CLASSIFICATION, COMPETITION_LEVEL,
    SNAPS_ESTIMATE, TRAINING_HRS, COACHING_HRS, WEIGHT_ROOM_DAYS,
    FILM_HRS, JOB_HRS, COMMUTE_MIN
)

def to_bool(x):
    if x is None:
        return pd.NA
    s = str(x).strip().lower()
    if s in {"true", "t", "yes", "y", "1"}:
        return True
    if s in {"false", "f", "no", "n", "0"}:
        return False
    return pd.NA

def ingest(input_csv: str, output_path: str):
    df = pd.read_csv(input_csv)

    df = df.rename(columns=RENAME_MAP)

from code.bin_mapping import HONORS_LABEL_TO_LEVEL

df["honors_level_num"] = df["honors_level"].apply(lambda x: HONORS_LABEL_TO_LEVEL.get(str(x).strip(), pd.NA))


missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns after rename: {missing}")


    # Consent gate
df["consent_ok"] = df["consent_acknowledged"].apply(consent_to_bool)
df = df[df["consent_ok"]].copy()

    # Assign random UUIDs at ingestion (no PII).
    df["player_id"] = [str(uuid.uuid4()) for _ in range(len(df))]

    # Core categorical -> numeric
    df["position_group_num"] = df["position_group"].apply(lambda x: map_cat(x, POSITION_GROUP))
    df["school_classification_num"] = df["school_classification"].apply(lambda x: map_cat(x, SCHOOL_CLASSIFICATION))
    df["competition_level_num"] = df["competition_level"].apply(lambda x: map_cat(x, COMPETITION_LEVEL))
    df["snaps_estimate_num"] = df["snaps_estimate"].apply(lambda x: map_cat(x, SNAPS_ESTIMATE))

    df["training_hours_num"] = df["training_hours_per_week"].apply(lambda x: map_cat(x, TRAINING_HRS))
    df["coaching_hours_num"] = df["coaching_hours_per_week"].apply(lambda x: map_cat(x, COACHING_HRS))
    df["weight_room_access_num"] = df["weight_room_access_days"].apply(lambda x: map_cat(x, WEIGHT_ROOM_DAYS))
    df["film_hours_num"] = df["film_hours_per_week"].apply(lambda x: map_cat(x, FILM_HRS))

    df["job_hours_num"] = df["job_hours_per_week"].apply(lambda x: map_cat(x, JOB_HRS))
    df["commute_minutes_num"] = df["commute_minutes"].apply(lambda x: map_cat(x, COMMUTE_MIN))
    df["missed_offseason_binary"] = df["missed_offseason_binary"].apply(to_bool)

    # Coerce ints where appropriate
    df["games_played"] = pd.to_numeric(df["games_played"], errors="coerce").astype("Int64")
    df["offseason_participation_weeks"] = pd.to_numeric(df["offseason_participation_weeks"], errors="coerce").astype("Int64")
    df["honors_level"] = pd.to_numeric(df["honors_level"], errors="coerce").astype("Int64")

    df["college_roster_binary"] = df["college_roster_binary"].apply(to_bool)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if output_path.endswith(".parquet"):
        df.to_parquet(output_path, index=False)
    else:
        df.to_csv(output_path, index=False)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    ingest(args.input, args.output)

if __name__ == "__main__":
    main()
