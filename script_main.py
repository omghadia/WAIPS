from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
import os
import urllib.parse
import joblib

def loadFile(name):
    directory = str(os.getcwd())
    filepath = os.path.join(directory, name)
    with open(filepath, 'r', encoding="utf8") as f:
        data = f.readlines()
    return list(set(str(urllib.parse.unquote(d.strip())) for d in data))

print("Loading files...")
badQueries = loadFile('badqueries2.txt')
goodQueries = loadFile('goodqueries2.txt')

print("Processing data...")
allQueries = badQueries + goodQueries
y = [1] * len(badQueries) + [0] * len(goodQueries)

print("Vectorizing text data...")
vectorizer = TfidfVectorizer(min_df=2, analyzer="char", sublinear_tf=True, ngram_range=(2, 5))
X = vectorizer.fit_transform(allQueries)

print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Training Bagging Model with Random Forest...")
bagging_model = BaggingClassifier(
    base_estimator=RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42),
    n_estimators=10,  # Number of base models
    max_samples=0.8,  # Fraction of data per model
    max_features=0.8,  # Fraction of features per model
    random_state=42
)
bagging_model.fit(X_train, y_train)

print("Saving model and vectorizer...")
joblib.dump(bagging_model, 'bagging_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

print("Making predictions...")
predicted = bagging_model.predict(X_test)

print("Evaluating performance...")
print("Accuracy: %f" % metrics.accuracy_score(y_test, predicted))
print("Precision: %f" % metrics.precision_score(y_test, predicted))
print("Recall: %f" % metrics.recall_score(y_test, predicted))
print("F1-Score: %f" % metrics.f1_score(y_test, predicted))
