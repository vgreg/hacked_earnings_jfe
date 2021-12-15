"""

Takes the raw text data from PR and merges it with the earnings data
for ML estimation. Also creates an alternative version from lemmatization.

"""

import os
import pandas as pd
from datetime import datetime

import nltk

pr_dir = "../Data/Press releases/"

txt_files = []

for y in ["2011", "2014", "2010", "2013", "2012", "2015"]:
    for q in ["QTR1", "QTR2", "QTR3", "QTR4"]:
        q_dir = pr_dir + "Press releases txt/" + y + "/" + q + "/"
        files = os.listdir(q_dir)
        files = [f for f in files if f.endswith(".txt")]

        for f in files:
            permno_str, dt_str, id_str = f.split(".")[0].split("_")
            permno = int(permno_str)
            pr_id = int(id_str.split(" ")[0])
            date = datetime.strptime(dt_str, "%Y%m%d")

            with open(q_dir + f) as file:
                txt = file.read()

            txt_files.append(
                {"PERMNO": permno, "date": date, "pr_id": pr_id, "text": txt}
            )

txt_df = pd.DataFrame(txt_files)

panel = pd.read_hdf("../Proprietary Data (cannot be shared)/MainPanel.hdf")

panel["date"] = pd.to_datetime(panel["date"])

merged = pd.merge(panel, txt_df, on=["PERMNO", "date"])

print(f"Pre clean len :{len(merged)}")

merged = merged.groupby(["PERMNO", "date"]).first()

print(f"Post clean len :{len(merged)}")


#%% Stop words removal and stemming

# First, we want to extract all the words in the text.
# The regexp_tokenize line will convert everything to lower cap, keep only words
# (i.e. drop numbers and ponctuation) and split everything in tokens.
#
# We also typically want to remove the stop words (frequent
# words like "a" and "the")
# We'll use the default english corpus stopwords, but
# first we need to download them if we haven't already.
# If it's the first time running this code, uncomment
# the last line and run. Then download the "stopwords"
# corpora.
# Note that for our purposes this doesn't make a
# difference, so you can skip the filtering on stop
# words.

# This line needs to be executed once to download NLTK packges
# nltk.download()


sr = nltk.corpus.stopwords.words("english")

def clean_text(text):
    tokens = []
    for t in nltk.regexp_tokenize(text.lower(), "[a-z]+"):
        if t not in sr:
            tokens.append(t)
    tokens[:10]

    # Next we  want to stem the words (remove the ending)
    stemmed_tokens = []
    for t in tokens:
        t = nltk.PorterStemmer().stem(t)
        stemmed_tokens.append(t)
    stemmed_tokens[:10]

    return pd.Series(
        {"text_clean": " ".join(tokens), "text_clean_stemmed": " ".join(stemmed_tokens)}
    )


merged[["text_clean", "text_clean_stemmed"]] = merged.text.apply(clean_text)

merged.to_parquet(pr_dir + "PR_panel.parquet")
