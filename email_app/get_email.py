import dotenv, imaplib, email, os
import pandas as pd
from email import utils
from datetime import date
import sys
sys.path.insert(1, "./preprocessing")
from clean_csv import *



def get_cred():
    """function to get var from env
    :param:
    :return dict: return a dict of credentials
    """

    # dotenv.load_dotenv("../../.env")
    dir_name = os.getcwd()
    env_path = os.path.join(dir_name, ".env")
    dotenv.load_dotenv(env_path)

    return {
        "user": os.environ.get("EUSER"),
        "pwd": os.environ.get("EPWD"),
        "url": os.environ.get("URL"),
    }


def init_imap(cred):
    """function to initialise imap obj using credential
    :param cred: dictionary of credentials to initialise imap
    :return corr: return imap object
    """
    try:
        corr = imaplib.IMAP4_SSL(cred["url"], 993)
        corr.login(cred["user"], cred["pwd"])
        corr.select("Inbox")
    except Exception as e:
        print(f"An error occured\n{e}")

    return corr


def get_all_email(imap):
    """function to get all emails
    :param imap: imap obj
    :return msgnums: return all email
    """

    _, msgnums = imap.search(None, "ALL")
    msgnums = msgnums[0].split()

    return msgnums


def get_body(msg):
    """function to get body
    :param msg: email
    :return content: return content of body
    """
    content = []

    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            content.append(part.as_string())

    return content


def get_emails(n, email_list, imap):
    tdy_date = date.today()
    counter = 0

    n = len(email_list) - int(n)

    email_df = pd.DataFrame(columns=["sender", "subject", "body"])

    try:
        for i in range(n, len(email_list)):
            _, data = imap.fetch(email_list[i], "(RFC822)")

            msg = email.message_from_bytes(data[0][1])
            e_date = msg.get("date")
            e_date = utils.parsedate_to_datetime(e_date).date()

            if e_date == tdy_date:
                counter += 1
                sender = msg.get("From")
                subject = msg.get("subject")
                body = get_body(msg)
                temp_df = pd.DataFrame(
                    {"sender": [sender], "subject": [subject], "body": [body]}
                )
                email_df = pd.concat([email_df, temp_df])

        return email_df

    except Exception as e:
        print(f"An error occured\n{e}")
        return email_df




if __name__ == "__main__":
    cred = get_cred()
    imap = init_imap(cred)
    emails = get_all_email(imap)
    get_mail = get_emails(50, emails, imap)
    save_to_file(get_mail, "./datas/today-data.csv", index=False)