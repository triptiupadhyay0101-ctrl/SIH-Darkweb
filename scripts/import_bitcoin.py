import pandas as pd

from app.database.connection import engine
from sqlalchemy import text


# Load dataset
df = pd.read_csv("data/bitcoin_entity_dataset.csv")

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", list(df.columns))


# Insert data into PostgreSQL
with engine.connect() as connection:

    for _, row in df.iterrows():

        connection.execute(
            text("""
                INSERT INTO bitcoin_entities
                (
                    record_id,
                    total_inflow_btc,
                    total_outflow_btc,
                    avg_tx_value,
                    tx_count_in,
                    tx_count_out,
                    active_duration_days,
                    in_out_ratio,
                    temporal_entropy,
                    address_count,
                    entity_label
                )
                VALUES
                (
                    :record_id,
                    :total_inflow_btc,
                    :total_outflow_btc,
                    :avg_tx_value,
                    :tx_count_in,
                    :tx_count_out,
                    :active_duration_days,
                    :in_out_ratio,
                    :temporal_entropy,
                    :address_count,
                    :entity_label
                )
            """),
            row.to_dict()
        )

    connection.commit()


print("Bitcoin dataset imported successfully!")