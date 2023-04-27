
from sklearn.feature_extraction.text import CountVectorizer
import joblib
from nltk.corpus import stopwords
import string


def check_spam(new_email):
    # Vectorize the email body text using the Bag-of-Words model
    CountVectorizer(analyzer=process_text)

    # Load the saved model and CountVectorizer from disk
    model = joblib.load('./machine_learning/spam_model.joblib')
    vectorizer = joblib.load('./machine_learning/vectorizer.joblib')

    # Load the new email into a string variable

    # Vectorize the new email using the same CountVectorizer
    new_email_vec = vectorizer.transform([new_email])

    # Use the trained model to predict the label of the new email
    prediction = model.predict(new_email_vec)[0]

    return prediction


def process_text(text):
    # 1 remove the punctuation
    # 2 remove stopwords (useless word or data)
    # 3 return a list of clean text words
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    # 2
    clean_words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    # 3
    return clean_words
