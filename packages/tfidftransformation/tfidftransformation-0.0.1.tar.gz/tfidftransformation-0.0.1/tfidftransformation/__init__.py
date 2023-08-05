import pandas as pd
import numpy as np
import re
import nltk
from collections import Counter
import scipy.sparse as sp
from numpy.linalg import norm


class TFIDF(object):
    def __init__(self, corpus):
        """
        This is a class for tf-idf transformation
        Parameters:
            corpus: the total document set
        """
        self.corpus = corpus
        self.norm_corpus = None
        # download stop words from nltk library
        nltk.download('stopwords')
        # download punkt tokenizer models
        nltk.download('punkt')

    @staticmethod
    def __normalize_corpus(d):
        """
        Normalizes corpus
        Parameters:
            d: corpus (total document set)
        Returns:
            normalized corpus
        """
        # TF-IDF can be sensitive to the presence of stop words, which are common words that occur frequently in most
        # documents and do not provide useful information. Because TF-IDF is based on the frequency of words in a
        # document, it can give higher weights to stop words if they occur frequently in the document. This can result
        # in stop words having a disproportionate influence on the overall representation of the document, which can be
        # detrimental to the performance of the model.
        # To mitigate this issue, I removed stop words from the documents before calculating the TF-IDF vectors. This
        # can help to reduce the influence of stop words on the vectors and improve the performance of the model.
        stop_words = nltk.corpus.stopwords.words('english')  # define stop words
        # remove characters other than alphanumeric (A-Za-z0-9) characters in input document
        d = re.sub(r'[^a-zA-Z0-9\s]', '', d, re.I | re.A)
        # convert lowercase and remove spaces at the beginning and at the end of the document
        d = d.lower().strip()
        # extract tokens from the document
        tks = nltk.word_tokenize(d, language='english', preserve_line=False)
        # remove stop words from the document
        f_tks = [t for t in tks if t not in stop_words]
        # combine and return tokens
        return ' '.join(f_tks)

    def preprocessing_text(self):
        """
        Preprocess text data
        """
        # vectorize normalized corpus
        n_c = np.vectorize(self.__normalize_corpus)
        self.norm_corpus = n_c(self.corpus)

    def tf(self):
        """
        Computes term frequency, which is calculated with this formula: (number of times the words appear in a document)
        / (total number of words in the document)
        Returns:
            tf: frequency of each word for each document
        """
        # extract words for all documents in corpus
        words_array = [doc.split() for doc in self.norm_corpus]
        # convert unique words to list
        words = list(set([word for words in words_array for word in words]))
        # define features dictionary
        features_dict = {w: 0 for w in words}
        # define term frequency
        tf = []
        # for each document in the corpus compute frequency of each word
        for doc in self.norm_corpus:
            # bag of words frequency of document
            bowf_doc = Counter(doc.split())
            # all number of words
            all_f = Counter(features_dict)
            # update bag of words frequency of document
            bowf_doc.update(all_f)
            # add bag of words to term frequency list
            tf.append(bowf_doc)
        return pd.DataFrame(tf)

    @staticmethod
    def df(tf):
        """
        Computes document frequency
        Parameters:
            tf: term frequency
        Returns:
            df: document frequency
        """
        features_names = list(tf.columns)
        df = np.diff(sp.csc_matrix(tf, copy=True).indptr)
        # 1 is added to the document frequency to prevent 0 division error
        df = 1 + df
        return df

    def idf(self, df):
        """
        Computes inverse document frequency
        Parameters:
            df: document frequency
        Returns:
            idf: inverse document frequency
            idf_d: inverse document frequency diagonal matrix
        """
        # length of corpus
        N = 1 + len(self.norm_corpus)
        # inverse document frequency function, 1 is added to the result, numerator and denominator to prevent
        # 0 division error, idf(df) = log[(1+n)/(1+df(t))]+1
        idf = (1.0 + np.log(float(N) / df))
        # rescale idf by multiplying it with a sparse diagonal matrix
        idf_d = sp.spdiags(idf, diags=0, m=len(df), n=len(df)).todense()
        return idf, idf_d

    @staticmethod
    def tfidf(tf, idf):
        """
        Computes tf-idf transformation
        Parameters:
            tf: term frequency
            idf: inverse document frequency
        Returns:
            normalized tf-idf transformation
        """
        # convert term frequency to numpy array
        tf = np.array(tf, dtype='float64')
        # compute tfidftransformation by multiplying tf and idf
        tfidf = tf * idf
        # define L2 norm of tfidftransformation
        norms = norm(tfidf, axis=1)
        # normalize final results using L2 norm
        return tfidf / norms[:, None]

# useful resources: https://github.com/makarandtapaswi/MovieQA_CVPR2016/blob/master/tfidf.py
