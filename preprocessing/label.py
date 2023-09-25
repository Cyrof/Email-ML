from clean_csv import *
import pandas as pd

def count_word(text_list):
    count = dict()

    for s in text_list:
        if s in count:
            count[s] += 1
        else:
            count[s] = 1
    
    return count

def check_kw_count(kw, word_count):
    kw_count = {key: 0 for key in kw}

    for key in word_count:
        for kw_key, val_list in kw.items():
            if key in val_list:
                kw_count[kw_key] += word_count[key]
            else:
                continue
    return kw_count

def label(kw_count):
    if all(value==0 for value in kw_count.values()):
        return "miscellaneous"
    else:
        return max(kw_count, key=kw_count.get)
    



def filter_label(keywords, df):
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
    n_df = pd.DataFrame(columns=["text", "label"])

    for ind in df.index:
        text = f"{df['Sender'][ind]} {df['Subject'][ind]} {df['Body'][ind]}"
        temp_df = pd.DataFrame({
            'text': text,
            'label': df['Label'][ind]
        }, index=[ind])
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