SNAPS_ESTIMATE = {
    "<200": 1,
    "200–500": 2, "200-500": 2,
    "500–800": 3, "500-800": 3,
    "800+": 4,
    "Don't know": -1,
    "unknown": -1
}

COMPETITION_LEVEL = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "low": 1, "medium": 2, "high": 3,
    "unknown": -1
}

SCHOOL_CLASSIFICATION = {
    "1A": 1, "2A": 2, "3A": 3, "4A": 4, "5A": 5, "6A": 6,
    "unknown": -1
}

TRAINING_HRS = {
    "<3": 1,
    "3-5": 2, "3–5": 2,
    "6-8": 3, "6–8": 3,
    "9+": 4,
    "unknown": -1
}
COACHING_HRS = TRAINING_HRS

WEIGHT_ROOM_DAYS = {
    "0": 0,
    "1-2 days": 1, "1–2 days": 1,
    "3-4 days": 2, "3–4 days": 2,
    "5+ days": 3, "5+": 3,
    "unknown": -1
}

FILM_HRS = {
    "0": 0,
    "<1": 1,
    "1-3": 2, "1–3": 2,
    "4 or more": 3, "4+": 3,
    "unknown": -1
}

JOB_HRS = {
    "0": 0,
    "1-5": 1, "1–5": 1,
    "6-10": 2, "6–10": 2,
    "11-20": 3, "11–20": 3,
    "20+": 4,
    "unknown": -1
}

COMMUTE_MIN = {
    "Less than 10 minutes": 1,
    "10-20 minutes": 2, "10–20 minutes": 2,
    "21-40 minutes": 3, "21–40 minutes": 3,
    "40+ minutes": 4,
    "unknown": -1
}

HONORS_LABEL_TO_LEVEL = {
    "None": 0,
    "Team Captain / Team Award": 1,
    "All-section/Third team": 2,
    "All-section/Second team": 3,
    "All-section/First team": 4,
    "All-Conference / All-Region": 5,
    "All-State": 6
}
