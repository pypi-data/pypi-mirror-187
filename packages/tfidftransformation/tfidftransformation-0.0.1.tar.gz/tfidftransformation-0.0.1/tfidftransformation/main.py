from tfidftransformation import TFIDF
import pandas as pd
import numpy as np


if __name__ == '__main__':
    corpus = [
        'This is the first document.',
        'This document is the second document.',
        'This is an another document.',
        'This is the last document.'
    ]

    # define TFIDF object
    obj = TFIDF(corpus)
    # preprocess set of documents
    obj.preprocessing_text()

    # calculate frequency of each word for each document (tf)
    tf = obj.tf()
    # calculate the number of documents in which the word w appear
    df = obj.df(tf)
    # compute inverse document frequency
    idf, idf_d = obj.idf(df)
    # compute tfidftransformation by normalizing tf and idf using L2 norm
    tfidf = obj.tfidf(tf, idf)
    # convert tfidftransformation to pandas dataframe and print results
    df = pd.DataFrame(np.round(tfidf, 2), columns=list(tf.columns))
    sorted_column_df = df.sort_index(axis=1)
    print(sorted_column_df)
