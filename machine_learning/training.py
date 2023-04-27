import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
from nltk.corpus import stopwords
import string
from nltk.tokenize.sonority_sequencing import punctuation
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
# import nltk
# nltk.download('stopwords')

def process_text(text):
  #1 remove the punctuation
  #2 remove stopwords (useless word or data)
  #3 return a list of clean text words
  nopunc = [char for char in text if char not in string.punctuation]
  nopunc = ''.join(nopunc)

  #2
  clean_words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

  #3
  return clean_words

# Load the spam.csv dataset
data = pd.read_csv('spam.csv')

# Vectorize the email body text using the Bag-of-Words model
vectorizer = CountVectorizer(analyzer=process_text)
X_vec = vectorizer.fit_transform(data['text'])

# Train a logistic regression model
model = LogisticRegression()
model.fit(X_vec, data['label_num'])

# Save the trained model and fitted CountVectorizer to disk
joblib.dump(model, 'spam_model.joblib')
joblib.dump(vectorizer, 'vectorizer.joblib')