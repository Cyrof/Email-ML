# from preprocessing import clean_csv, label, process
import sys
sys.path.insert(1, "./preprocessing")
from clean_csv import *
from process import *

def get_df():
    df = to_df("./datas/today-data.csv")
    return df

def level_1_clean(df):
    rm_na_df = remove_null(df)
    p_b_df = process_body(rm_na_df)
    p_sub_df = process_sub(p_b_df)
    p_send_df = process_sender(p_sub_df)

    return p_send_df

def level_2_clean(df):
    pass

