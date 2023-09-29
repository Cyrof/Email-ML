import pandas as pd
import re
import enchant
import email.header

def to_df(csv_path, index=True):
    """ function to get csv data into dataframe
    :param csv_path: path to csv file
    :return df: return dataframe of the csv data
    """
    if index:
        df = pd.read_csv(csv_path, index_col=[0])
    else:
        df = pd.read_csv(csv_path)

    return df

def remove_null(df):
    """ function to remove rows if column/s is empty
    :param df: dataframe of data
    :return df: return dataframe after removing null rows
    """
    df.dropna(
        axis=0,
        inplace=True,
    )
    return df

def save_to_file(df, path, index=True):
    df.to_csv(path, index=index)
    print("data saved")

def process_body(df):
    """ function to process dataframe body data
    :param df: dataframe
    :return df: return processed df
    """
    # bod = df["Body"].iloc[0]
    # bod = bod.split("\n\n")
    # bod = [elem.replace("\n", '') for elem in bod]
    # bod = " ".join(bod)
    # pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    # bod = re.sub(pattern, '', bod)
    # print(bod)
    
    for i in range(len(df)):
        bod = df.iloc[i]["Body"].split("\n\n")
        bod = " ".join([elem.replace("\n", '') for elem in bod])
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        bod = re.sub(pattern, '', bod)
        bod = " ".join(elem.lower() for elem in bod.split())
        print(bod)

        df.iloc[i]["Body"] = bod
    
    return df

def process_sub(df):
    # sub = df["Subject"].iloc[0]
    # sub = re.sub(r'[^\w_]+', ' ', sub)
    # sub = email.header.decode_header(sub)[0][0]
    # print(sub)

    for i in range(len(df)):
        sub = df.iloc[i]["Subject"]
        sub = email.header.decode_header(sub)[0][0]
        if type(sub) == bytes:
            sub = sub.decode('utf-8', errors='ignore')
        sub = re.sub(r'[^\w_]+', ' ', sub)
        sub = " ".join([elem.lower() for elem in sub.split()])
        
        # sub = " ".join(w.lower() for w in sub.split() if not any(x.isdigit() for x in w))

        df.iloc[i]["Subject"] = sub
    
    return df

def process_sender(df):
    # sender = df["Sender"].iloc[0]
    # sender = re.sub(r'[<>"\']', '', sender)
    # print(sender)
    for i in range(len(df)):
        sender = df.iloc[i]["Sender"]
        sender = sender.split()
        try:
            sender[0] = email.header.decode_header(sender[0])[0][0]
            if type(sender[0]) == bytes:
                sender[0] = sender[0].decode('utf-8', errors='ignore')
        except Exception as e:
            print(e)
        
        sender = re.sub(r'[<>"()\']', '', " ".join([elem.lower() for elem in sender]))
        
        # sender = re.sub(r'[<>"\']', '', str(sender))
        # if type(sender) == bytes:
        #     sender = sender.decode('utf-8', errors='ignore')
        

        df.iloc[i]["Sender"] = sender
    
    return df

if __name__ == "__main__":
    # this file contains function that is required in the main.py file for the whole program to run 

    
    og_df = to_df("./datas/emails.csv", index=False) # og df
    rm_na_df = remove_null(og_df) # remove null val from df
    p_b_df = process_body(rm_na_df) # process body from df
    p_sub_df = process_sub(p_b_df) # process subject from df
    p_send_df = process_sender(p_sub_df) # process sender from df
    save_to_file(p_send_df, "./datas/processed-data.csv") # save df to file