import pandas as pd
import joblib
import sys
sys.path.insert(1, './preprocessing')
from clean_csv import *
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.feature_extraction.text import CountVectorizer

def tts(df):
    """ Function to do train test split for ml
    :param df:
    :return [x_train, x_test, y_train, y_test]: return x train and test val & x train and test val
    """
    x = df["text"]
    y = df["label"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=df['label'], random_state=123)

    return [x_train, x_test, y_train, y_test]

def save_cv(obj):
    joblib.dump(obj, 'cv.pkl')
    print("feature saved")

def feature_extraction(split_val):
    """ function to do feature extraction
    :param split_val: list of x & y train/test
    :return split_val: return updated list of x & y train/test
    """
    cv = CountVectorizer(
        ngram_range=(1, 3),
        stop_words="english",
    )

    x_train_cv = cv.fit_transform(split_val[0])
    x_test_cv = cv.transform(split_val[1])

    split_val[0] = x_train_cv
    split_val[1] = x_test_cv
    save_cv(cv)

    return split_val

def save_model(model):
    """ function to save model into pickle file 
    :param model:  machine learning model
    :return: 
    """
    joblib.dump(model, 'model_tc.pkl')
    print("Model saved")

def create_model(scores, models, train_test):
    """ function to create machine learning model based on highest accurary score
    :param scores: dictionary of models with their acc scores
    :param models: list of tuple containing model name and model instance
    :param train_test: list of x&y train/test
    :return:
    """

    highest_key = max(scores, key=scores.get)
    models = dict(models)
    model = models[highest_key].fit(train_test[0], train_test[2])

    print(highest_key)
    print(f1_score(train_test[3], model.predict(train_test[1]), average='weighted'))

    save_model(model)


def compare_model_acc(models, train_test):
    """ function to get all model accuracy
    :param models: list of tuples containing model name and model instance
    :param train_test: list of x&y train/test
    :return:
    """
    score = {}
    for name, model in models:
        print(name)
        model.fit(train_test[0], train_test[2])
        predict = model.predict(train_test[1])
        score[name] = f1_score(train_test[3], predict, average='weighted')


    create_model(score, models, train_test)



if __name__ == "__main__":
    # functions in this file is not required in the main.py file 
    
    models = [
        ('LR', LogisticRegression(solver='liblinear')),
        ('NB', MultinomialNB()),
        ('RF', RandomForestClassifier(n_estimators=10))
    ]

    df = to_df("./datas/latest-data.csv")
    train_test = tts(df)
    train_test = feature_extraction(train_test)
    compare_model_acc(models, train_test)