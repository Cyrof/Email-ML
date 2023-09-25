from clean_csv import *
import nltk
nltk.download("all")
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def lemmatize_r_stopword(df):
    lemmatizer = WordNetLemmatizer()
    text = list(df['text'])
    corpus = []

    for i in range(len(text)):
        r = re.sub(r'[/=#:;"()-+\']', ' ', text[i])
        r = r.split()
        r = [word for word in r if word not in stopwords.words('english')]
        r = " ".join([lemmatizer.lemmatize(word) for word in r])
        corpus.append(r)

        print(f"Remove stopwords and lemmatized {i}")
    
    df['text'] = corpus
    return df
        



if __name__ == "__main__":
    # this file contains important function that is required in the main.py file for the program to run 
    
    df = to_df("./datas/labeled-data.csv", index=True)
    l_sw_df = lemmatize_r_stopword(df)
    save_to_file(l_sw_df, "./datas/latest-data.csv")
    # print(l_sw_df)