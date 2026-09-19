import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

# 1. Load the dataset we generated
df = pd.read_csv("spam_dataset.csv")

# 2. Build a pipeline: TF-IDF turns text into numeric vectors,
#    MultinomialNB is a classifier that works well on word-count-like features
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB()),
])

# 3. Train on the whole dataset (simple assignment, no need for a train/test split
#    unless your rubric asks for accuracy reporting)
pipeline.fit(df["text"], df["label"])

# 4. Persist the trained pipeline to disk so the API can load it at startup
joblib.dump(pipeline, "model.joblib")
print("Saved model.joblib")