import sys
from preprocessing import clean_csv, process
from email_app import get_email



if __name__ == "__main__":
    # print(clean_csv.to_df("./datas/today-data.csv"))
    print(clean_csv.to_df("./datas/today-data.csv", index=False))