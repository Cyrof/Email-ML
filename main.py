import sys
from preprocessing import clean_csv, process
from email_app import get_email, process_data
import log

def get_today_email():
    cred = get_email.get_cred()
    imap = get_email.init_imap(cred)
    emails = get_email.get_all_email(imap)
    get_current_mail = get_email.get_emails(50, emails, imap)
    rm_list = get_email.remove_list(get_current_mail)
    clean_csv.save_to_file(rm_list, "datas/today-data.csv", index=False)

def clean_data():
    df = process_data.get_df()
    n_df = process_data.level_1_clean(df)
    print(n_df)

if __name__ == "__main__":
    # print(clean_csv.to_df("./datas/today-data.csv"))
    # get_today_email()
    clean_data()
    pass