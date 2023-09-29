# from preprocessing import clean_csv, label, process
import sys
sys.path.insert(1, "./preprocessing")
from clean_csv import *
from process import *
import pandas as pd
import re

def get_df():
    """ function to get df from file
    :param:
    :return df: return df 
    """
    df = to_df("./datas/today-data.csv", index=False)
    return df

def process_body(df):
    """ function to process body
    :param df: dataframe to process
    :return df: return df after processing body 
    """
    # bod = df.iloc[0]["Body"]
    # pattern = r'http\S+|www.\S+|\[.*?\]|\W+'
    # bod = re.sub(pattern, ' ', bod)
    # bod = " ".join([elem for elem in bod.split() if not any(x.isdigit() for x in elem)])

    for i in range(len(df)):
        bod = df.iloc[i]["Body"]
        pattern = r'http\S+|www.\S+|\[.*?\]|\W+'
        bod = re.sub(pattern, ' ', bod)
        bod = " ".join([elem.lower() for elem in bod.split() if not any(x.isdigit() for x in elem)])

        df.iloc[i]["Body"] = bod
    return df

def level_1_clean(df):
    """ function to do level 1 cleaning 
    :param df: df to clean
    :return p_send_df: return df after cleaning
    """
    rm_na_df = remove_null(df)
    print("Null removed")
    p_b_df = process_body(rm_na_df)
    print("level 1 body processed")
    p_sub_df = process_sub(p_b_df)
    print("level 1 subject proccessed")
    p_send_df = process_sender(p_sub_df)

    return p_send_df

def level_2_clean(df):
    """ function to do level 2 cleaning
    :param df: df to clean
    :return l_sw_df: return processed df
    """
    n_df = pd.DataFrame(columns=["sender", "subject", "text"])
    for i in range(len(df)):
        text = f"{df.iloc[i]['Sender']} {df.iloc[i]['Subject']} {df.iloc[i]['Body']}"
        temp_df = pd.DataFrame({'sender': df.iloc[i]['Sender'], 'subject': df.iloc[i]['Subject'], 'text': text}, index=[i])
        n_df = pd.concat([n_df, temp_df])

    l_sw_df = lemmatize_r_stopword(n_df)

    return l_sw_df

