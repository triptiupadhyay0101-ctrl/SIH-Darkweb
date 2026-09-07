import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import joblib

from app.database.connection import engine


print("Loading stylometry data...")

df = pd.read_sql(
    "SELECT author_id, text FROM stylometry_texts",
    engine
)

df = df.dropna(subset=["author_id", "text"])
df = df.sample(
    n=min(5000, len(df)),
    random_state=42
)

print("Records:", len(df))
print("Authors:", df["author_id"].nunique())


model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            analyzer="char",
            ngram_range=(3, 4),
            min_df=2,
            max_features=10000
        )
    ),
    (
        "classifier",
        LinearSVC(
            max_iter=1000
        )
    )
])


print("Training model...")

model.fit(
    df["text"],
    df["author_id"]
)


joblib.dump(
    model,
    "stylometry_model.joblib"
)

print("Stylometry model trained successfully!")
print("Model saved as stylometry_model.joblib")