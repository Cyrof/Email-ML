from clean_csv import *
import pandas as pd

def count_word(text_list):
    """ function to count the amount of word appearance
    :param text_list: list of text
    :return count: return text appearance count
    """
    count = dict()

    for s in text_list:
        if s in count:
            count[s] += 1
        else:
            count[s] = 1
    
    return count

def check_kw_count(kw, word_count):
    """ function to check word in keyword and total count of word appearance
    :param kw: dict of keywords
    :param word_count: count of all word appearance
    :return kw_count: return words from keyword ans total count of appearance
    """
    kw_count = {key: 0 for key in kw}

    for key in word_count:
        for kw_key, val_list in kw.items():
            if key in val_list:
                kw_count[kw_key] += word_count[key]
            else:
                continue
    return kw_count

def label(kw_count):
    """ function to label text
    :param kw_count: dict of keyword with total appearance count
    :return label: return the label of the text based on appearance count
    """
    if all(value==0 for value in kw_count.values()):
        return "miscellaneous"
    else:
        return max(kw_count, key=kw_count.get)
    



def filter_label(keywords, df):
    """ funtion to label each text in df
    :param keyword: dict of keywords to label text
    :param df: dataframe of process data
    :return df: return labeled df
    """
    # label_sender(keywords, df["Sender"].iloc[5908])
    # print(df.head())
    # text = f"{df['Sender'].iloc[5908]} {df['Subject'].iloc[5908]} {df['Body'].iloc[5908]}"
    # text = text.split()
    # count = count_word(text)
    # kw_count = check_kw_count(keywords, count)
    # print(label(kw_count))

    for ind in df.index:
        text = f"{df['Sender'][ind]} {df['Subject'][ind]} {df['Body'][ind]}".split()
        count = count_word(text)
        kw_count = check_kw_count(keywords, count)
        row_label = label(kw_count)

        df.loc[ind, ['Label']] = row_label
    
    return df

def new_df(df):
    """ function to create new dataframe
    :param df: dataframe
    :return n_df: return new dataframe
    """
    n_df = pd.DataFrame(columns=["text", "label"])

    for i in range(len(df)):
        text = f"{df.iloc[i]['Sender']} {df.iloc[i]['Subject']} {df.iloc[i]['Body']}"
        temp_df = pd.DataFrame({
            'text': text,
            'label': df.iloc[i]['Label']
        }, index=[i])
        n_df = pd.concat([n_df, temp_df])
    
    return n_df

if __name__ == "__main__":
    # functions in this file is not required in the main.py file 
    
    """ 
    reservation 
    leisure -- youtube, spotify 
    games -- ???
    bills -- ??
    shopping
    """
    keywords = {
        "school" : ["murdoch", "mymurdoch", "kaplan", "student", "learning", "echo360", "zoom", "ms"],
        "work" : ["github", "docker", "dockerhub", "clickup", "repository"],
        "leisure": ["youtube", "twitter"],
        "games": ["genshin", "game"],
        "bills": ["myrepublic", "payment", "receipt", "purchases"],
        "shopping": ["qoo10", "order", "shipment"],
        "reservation": ["tix", "ticket", "booking", "gv"],
    }

    df = to_df("datas/processed-data.csv", index=True)
    filter_df = filter_label(keywords, df)
    n_df = new_df(filter_df)
    save_to_file(n_df, "./datas/labeled-data.csv")