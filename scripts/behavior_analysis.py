import pandas as pd

CSV_FILE = "data/bitcoin_entity_dataset.csv"

print("Loading Bitcoin behavioral data...")

df = pd.read_csv(CSV_FILE)

# Select behavioral features
features = [
    "tx_count_in",
    "tx_count_out",
    "active_duration_days",
    "in_out_ratio",
    "temporal_entropy",
    "avg_tx_value"
]

# Calculate normalized scores
for feature in features:
    min_value = df[feature].min()
    max_value = df[feature].max()

    if max_value != min_value:
        df[feature + "_score"] = (
            (df[feature] - min_value)
            / (max_value - min_value)
        )
    else:
        df[feature + "_score"] = 0

score_columns = [feature + "_score" for feature in features]

df["behavior_score"] = (
    df[score_columns].mean(axis=1) * 100
)

print("Behavioral analysis completed!")

print(
    df[
        ["record_id", "entity_label", "behavior_score"]
    ].head()
)
df[
    ["record_id", "entity_label", "behavior_score"]
].to_csv(
    "data/behavior_scores.csv",
    index=False
)

print("Behavior scores saved to data/behavior_scores.csv")