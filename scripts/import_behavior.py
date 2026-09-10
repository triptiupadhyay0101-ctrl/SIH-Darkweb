import pandas as pd
from sqlalchemy import text

from app.database.connection import engine

CSV_FILE = "data/behavior_scores.csv"

print("Loading behavioral scores...")

df = pd.read_csv(CSV_FILE)

print("Rows:", len(df))

records = df[
    ["record_id", "entity_label", "behavior_score"]
].to_dict("records")

with engine.begin() as connection:
    connection.execute(
        text("""
            INSERT INTO behavioral_scores
            (record_id, entity_label, behavior_score)
            VALUES
            (:record_id, :entity_label, :behavior_score)
        """),
        records
    )

print("Behavioral scores imported successfully!")