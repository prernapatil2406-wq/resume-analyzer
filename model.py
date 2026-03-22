import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# load dataset
data = pd.read_csv("dataset.csv")

X = data["skills"]
y = data["role"]

# convert text to numbers
vectorizer = CountVectorizer()
X_vector = vectorizer.fit_transform(X)

# train model
model = LogisticRegression()
model.fit(X_vector, y)

def predict_role(skills_text):
    skills_vector = vectorizer.transform([skills_text])
    prediction = model.predict(skills_vector)
    return prediction[0]
    