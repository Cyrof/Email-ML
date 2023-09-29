import sys
from preprocessing import clean_csv, process # local lib
from email_app import get_email, process_data, tele_bot # local lib 
import log
import pickle
import joblib
from sklearn.feature_extraction.text import CountVectorizer
import os
import time
import json
import numpy as np
import requests

def get_today_email():
    """ function to get current date email
    :param:
    :return:
    """
    cred = get_email.get_cred()
    imap = get_email.init_imap(cred)
    emails = get_email.get_all_email(imap)
    get_current_mail = get_email.get_emails(50, emails, imap, date_dev=(2023, 9, 29))
    rm_list = get_email.remove_list(get_current_mail)
    clean_csv.save_to_file(rm_list, "./datas/today-data.csv", index=False)

def clean_data():
    """ function to clean data from file
    :param:
    :return:
    """
    df = process_data.get_df()
    lvl1_df = process_data.level_1_clean(df)
    lvl2_df = process_data.level_2_clean(lvl1_df)
    
    clean_csv.save_to_file(lvl2_df, "./datas/today-data.csv")

def convert_numeric(text):
    """ function to use feature extraction to convert words to numerical value
    :param text: text to convert
    :return text: return converted text
    """
    cv = joblib.load("cv.pkl")
    text = cv.transform(text)
    return text

def email_predict():
    """ function to predict email
    :param:
    :return:
    """
    ml_model = joblib.load('model_tc.pkl')
    df = process_data.get_df()

    result = dict()

    for i in range(len(df)):
        text = convert_numeric([df.iloc[i]['text']])
        predict = ml_model.predict(text)
        # print(predict.item())

        result[i] = {
            'sender' : df.iloc[i]['sender'],
            'subject': df.iloc[i]['subject'],
            'prediction': predict.item()
        }
    save_result(result)

def save_result(results):
    json_data = json.dumps(results, indent=6)
    with open('./datas/results.json', 'w') as f:
        f.write(json_data)
        f.close()

    print("results saved")

def main():
    get_today_email()
    clean_data()
    time.sleep(2)
    os.system('clear')
    print("predicting emails...")
    email_predict()

if __name__ == "__main__":
    # get_today_email()
    # clean_data()
    # time.sleep(2)
    # os.system('clear')
    # print("predicting emails...")
    # email_predict()
    tele_bot.main()
    pass