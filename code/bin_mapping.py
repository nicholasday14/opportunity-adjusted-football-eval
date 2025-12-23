# code/bin_mapping.py

def normalize(x):
    if x is None:
        return None
    s = str(x).strip()
    if s == "" or s.lower() in {"na", "n/a", "none", "null", "unknown"}:
        return "unknown"
    return s

def map_cat(x, mapping, unknown_value=-1):
    s = normalize(x)
    if s is None:
        return unknown_value
    return mapping.get(s, unknown_value)

POSITION_GROUP = {
    "QB": 1, "RB": 2, "WR": 3, "OL": 4, "DL": 5, "LB": 6, "DB": 7, "ST": 8
}

SCHOOL_CLASSIFICATION = {
    "1A": 1, "2A": 2, "3A": 3, "4A": 4, "5A": 5, "6A": 6, "unknown": -1
}

COMPETITION_LEVEL = {"low": 1, "medium": 2, "high": 3, "unknown": -1}

SNAPS_ESTIMATE = {"<200": 1, "200–500": 2, "200-500": 2, "500–800": 3, "500-800": 3, "800+": 4, "unknown": -1}

TRAINING_HRS = {"<3": 1, "3–5": 2, "3-5": 2, "6–8": 3, "6-8": 3, "9+": 4, "unknown": -1}
COACHING_HRS = TRAINING_HRS

WEIGHT_ROOM_DAYS = {"0": 0, "1–2": 1, "1-2": 1, "3–4": 2, "3-4": 2, "5+": 3, "unknown": -1}

FILM_HRS = {"0": 0, "<1": 1, "1–3": 2, "1-3": 2, "4+": 3, "unknown": -1}

JOB_HRS = {"0": 0, "1–5": 1, "1-5": 1, "6–10": 2, "6-10": 2, "11–20": 3, "11-20": 3, "20+": 4, "unknown": -1}
COMMUTE_MIN = {"<10": 1, "10–20": 2, "10-20": 2, "21–40": 3, "21-40": 3, "40+": 4, "unknown": -1}

# Honors is already ordinal in your schema; keep as numeric.
# If your form collects labels instead, map labels to these numbers.

