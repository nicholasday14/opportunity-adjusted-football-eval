# code/data_ingest.py

import argparse
import os
import uuid
import pandas as pd

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
