import pandas as pd
from sqlalchemy import text

from app.database.connection import engine


CSV_FILE = "data/authorship_detection_kazakh_text.csv"

print("Loading stylometry dataset...")

df = pd.read_csv(
    CSV_FILE,
    encoding="utf-8-sig"
)

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", list(df.columns))


# Prepare data in batches
records = []

for _, row in df.iterrows():
    records.append({
        "author_id": str(row["author_id"]),
        "text": str(row["text"]),
        "source": "authorship_detection_kazakh_text"
    })


print("Prepared", len(records), "records.")
print("Starting database import...")


with engine.begin() as connection:

    batch_size = 1000

    for i in range(0, len(records), batch_size):

        batch = records[i:i + batch_size]

        connection.execute(
            text("""
                INSERT INTO stylometry_texts
                (author_id, text, source)
                VALUES
                (:author_id, :text, :source)
            """),
            batch
        )

        print(
            f"Imported {min(i + batch_size, len(records))}/{len(records)}"
        )


print("Stylometry dataset imported successfully!")