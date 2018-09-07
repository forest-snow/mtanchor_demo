import re
from sklearn.feature_extraction.text import CountVectorizer
import scipy.sparse
import numpy
from . import utils

def tokenize_en(text):
    """A basic English tokenizer which splits and does basic filtering.
    The included filters and transformations include:
    * lower case each token
    * filter out non-alphabetic characters for English
    """
    tokens = text.split()
    lowercase_tokens = [token.lower() for token in tokens]
    filtered_tokens = [re.sub(r'[^a-z]', '', token) for token in lowercase_tokens]
    english_tokens = [token for token in filtered_tokens if token != '']
    return english_tokens

def tokenize_zh(text):
    """A basic Chinese tokenizer which splits and does basic filtering.
    The included filters and transformations include:
    * filter out non-chinese characters for Chinese
    """
    tokens = text.split()
    filtered_tokens = [re.sub(r'[^\u4e00-\u9fff]', '', token) for token in tokens]
    chinese_tokens = [token for token in filtered_tokens if token != '']
    return chinese_tokens

def sparse_tranpose(doc_word):
    # Construct as COO matrix and then convert to CSC for sake of time
    doc_word_sparse = scipy.sparse.coo_matrix(doc_word)
    word_doc_sparse = doc_word_sparse.T
    word_doc = word_doc_sparse.tocsc()
    return word_doc

def vectorize(docs_train, stopwords, language, max_vocab, max_df, docs_dev=None, docs_test=None):
    print('vectorizing')
    """ Vectorizes words in documents so that vocabulary
    only contains words with document frequency of no more than [max_df].
    Then, vocabulary is filtered so that only the most frequent [max_vocab]
    words are in the set.
    """

    if language == 'en':
        tokenizer = tokenize_en
    else:
        tokenizer = tokenize_zh


    cv = CountVectorizer(tokenizer=tokenizer, 
        stop_words=stopwords, max_features=max_vocab,
        max_df=max_df)
    doc_word_train = cv.fit_transform(doc for doc in docs_train)
    word_doc_train = sparse_tranpose(doc_word_train)
    index = utils.numpy_to_int_dict(cv.vocabulary_)
    vocab = cv.get_feature_names()

    if docs_dev is not None:
        doc_word_dev = cv.transform(doc for doc in docs_dev)
        word_doc_dev = sparse_tranpose(doc_word_dev)
    if docs_test is not None:
        doc_word_test = cv.transform(doc for doc in docs_test)
        word_doc_test = sparse_tranpose(doc_word_test)

    return word_doc_train, word_doc_dev, word_doc_test, index, vocab 





