# Ethics & Privacy Framework

## Purpose
This project is designed as a decision-support system to assist early-stage football prospect evaluation. It does not replace human judgment, make recruiting decisions, or rank athletes.

## Participants
Participants are high school football players. All participants must provide informed consent. Where required, parental or guardian consent is mandatory.

## Data Minimization
Only data strictly necessary for modeling opportunity-adjusted evaluation is collected. The project explicitly excludes:
- Race, ethnicity, religion
- Family income or financial hardship
- Medical, mental health, or trauma history
- Any protected personal attributes

## De-identification
All modeling data uses anonymized player IDs. Names, schools, and contact information are stored separately and are never included in training data.

## Access Control
- Modeling datasets are anonymized and used only for research.
- Identifying information is restricted and not shared externally.
- No third-party access is granted to raw player data.

## Model Use Restrictions
The system may:
- Flag players for further human evaluation
- Estimate uncertainty-aware projections
- Simulate hypothetical support increases

The system may not:
- Make final recruiting decisions
- Label players as low potential or low ceiling
- Penalize players for opportunity constraints

## Transparency
All outputs include uncertainty estimates and explanations of contributing factors. Limitations and sources of bias are documented.

## Fairness Monitoring
Post-hoc audits are conducted to evaluate calibration and error patterns across resource-level groups. Detected harms are documented and addressed.

## Data Retention
Participants may request data removal at any time. Removed data will not be used in future analyses.
