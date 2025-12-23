# Data Schema (V1)

## Identifiers
- player_id (string): Random UUID assigned at ingestion; no identifying information
- position_group (categorical): QB, RB, WR, OL, DL, LB, DB, ST

## Performance Metrics
- games_played (int): Number of games participated in during the season
- snaps_estimate (categorical): <200, 200–500, 500–800, 800+, or unknown
- primary_production_stat (string): Raw primary stat entered with stat name (e.g., rushing yards, tackles, pressures)

## Team & Competition Context
- school_classification (categorical): 1A, 2A, 3A, 4A, 5A, 6A, unknown
- competition_level (categorical): low, medium, high
- team_record_or_win_pct (string): Wins–losses or win percentage

## Development Inputs
- training_hours_per_week (categorical): <3, 3–5, 6–8, 9+
- coaching_hours_per_week (categorical): <3, 3–5, 6–8, 9+
- weight_room_access_days (categorical): 0, 1–2, 3–4, 5+
- film_hours_per_week (categorical): 0, <1, 1–3, 4+
- offseason_participation_weeks (int): Weeks of structured offseason participation in last 12 months

## Opportunity Constraints
- job_hours_per_week (categorical): 0, 1–5, 6–10, 11–20, 20+
- commute_minutes (categorical): <10, 10–20, 21–40, 40+
- missed_offseason_binary (bool): True if missed ≥4 consecutive offseason weeks for non-injury reasons

## Honors & Recognition
- honors_level (ordinal categorical):
  - 0 = None
  - 1 = Team Captain / Team Award
  - 2 = All-Section / Third Team
  - 3 = All-Section / Second Team
  - 4 = All-Section / First Team
  - 5 = All-Conference / All-Region
  - 6 = All-State

## Outcome Labels
- college_roster_binary (bool): Whether the player appeared on a college roster
- college_level (categorical): P5, G5, FCS, none
- year1_snaps_bucket (categorical): none, low, medium, high

## Notes & Assumptions
- All non-outcome variables are measured at the high school level.
- Self-reported inputs are treated as noisy and non-causal.
- Outcome labels may reflect exposure bias and are interpreted accordingly.
- Models will report uncertainty and avoid deterministic or causal claims.

## Schema JSON
{
  "version": "v1",
  "required_columns": [
    "position_group",
    "games_played",
    "snaps_estimate",
    "primary_production_stat",
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
    "honors_level",
    "college_roster_binary",
    "college_level",
    "year1_snaps_bucket"
  ]
}
