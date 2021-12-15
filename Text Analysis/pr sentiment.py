"""
Estimates the ElasticNet models based on press releases words.
"""

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import ElasticNetCV

import pandas as pd

#%% Load dataset
pr_dir = "/data/vincent/data/Press releases/"
pr_df = pd.read_parquet(
    pr_dir + "PR_panel.parquet", columns=[text_col, "LRet_12pm_OpenNext"]
)
#%%%


def limit_words(text, word_limit):
    return " ".join(text.split(" ")[:word_limit])


def fit_reg_model(
    pr_df, regr, text_col, word_limit, min_df_ratio, max_df_ratio, out_fn
):
    text_train = pr_df[text_col].apply(lambda x: limit_words(x, word_limit))

    y_train = pr_df.LRet_12pm_OpenNext

    N = len(text_train)

    max_df = np.int64(np.floor(max_df_ratio * N))
    min_df = np.int64(np.floor(min_df_ratio * N))

    vect = CountVectorizer(min_df=min_df, max_df=max_df).fit(text_train)

    X_train = vect.transform(text_train)

    # Estimation
    regr.fit(X_train, y_train)

    y_fitted = regr.predict(X_train)

    out_df = pr_df[[]].copy()
    out_df["fitted"] = y_fitted

    out_df.to_parquet(pr_dir + "fitted/" + out_fn)

    df = pd.DataFrame([vect.get_feature_names(), regr.coef_]).T
    df.columns = ["word", "coef"]
    df["coef"] = np.float64(df["coef"])

    df = df.sort_values(["coef"])

    df.to_parquet(pr_dir + "fitted/" + out_fn[:-8] + "_WORDS.parquet")


fit_reg_model(
    pr_df,
    regr=ElasticNetCV(cv=5, l1_ratio=0.5, max_iter=10000),
    text_col=["text_clean_stemmed"],
    word_limit=400,
    min_df_ratio=0.005,
    max_df_ratio=0.4,
    out_fn="PR_fit_EN_0_5_text_clean_stemmed_400_Count_0_005_0_4_WORDS.parquet",
)
