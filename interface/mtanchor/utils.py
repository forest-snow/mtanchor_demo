import numpy 

def convert_2dlist(lst, index):
    new_lst = []
    for row in lst:
        new_row = []
        for entry in row:
            new_row.append(index[entry])
        new_lst.append(new_row)
    return new_lst

def get_top_topic_words(A, n, vocab=None):
    """Return top [n] words for every topic with information about probability
    distribution provided by [A].
    If [vocab] is not None, convert indices to words.
    """  
    assert n <= A.shape[0], \
        'Number of words requested greater than model\'s number of words'
    topic_words = A.T

    # sort words based on probabilities
    sort_words = numpy.argsort(topic_words, axis=1)
    # reverse so that the higher probabilities come first
    rev_words = numpy.flip(sort_words, axis=1)
    # retrieve top n words
    top_words = rev_words[:,:n]

    if vocab is None:
        return top_words
    else:
        top_words = convert_2dlist(top_words, vocab)
        return top_words

def numpy_to_int_dict(numpy_dict):
    int_dict = {k: int(v) for k, v in numpy_dict.items()}
    return int_dict

