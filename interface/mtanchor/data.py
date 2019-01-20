from .preprocess import vectorize
import os

data_path = '/Users/myuan/data/'

stopword_files = {
    'en':os.path.join(data_path,'stopwords/stopwords_en.txt'),
    'zh':os.path.join(data_path,'stopwords/stopwords_zh.txt'),
    'ru':os.path.join(data_path,'stopwords/stopwords_ru.txt')
}

wiki_shorts_en = {
    'docs':os.path.join(data_path,'wiki_shorts/en/corpus/docs.txt'),
    'labels':os.path.join(data_path,'wiki_shorts/en/labels.txt'),
    'train':os.path.join(data_path,'wiki_shorts/en/splits/train-7730.txt'),
    'dev':os.path.join(data_path,'wiki_shorts/en/splits/dev-1104.txt'),
    'max_vocab':1000,
    'max_df':0.07
}

wiki_shorts_zh = {
    'docs':os.path.join(data_path,'wiki_shorts/zh/corpus/docs.txt'),
    'labels':os.path.join(data_path,'wiki_shorts/zh/labels.txt'),
    'train':os.path.join(data_path,'wiki_shorts/zh/splits/train-7095.txt'),
    'dev':os.path.join(data_path,'wiki_shorts/zh/splits/dev-1013.txt'),
    'max_vocab':1000,
    'max_df':0.07
}

lorelei_ru = {}

lorelei_ru['ru'] = {
    'docs':os.path.join(data_path,'lorelei/il8/ru/corpus.txt'),
    'labels':os.path.join(data_path,'lorelei/il8/ru/labels.txt'),
    'train':os.path.join(data_path,'lorelei/il8/ru/splits/train-401.txt'),
    'dev':os.path.join(data_path,'lorelei/il8/ru/splits/dev-37.txt'),
    'max_vocab':6000,
    'max_df':0.7    
}

lorelei_ru['en'] = {
    'docs':os.path.join(data_path,'lorelei/il8/en/corpus.txt'),
    'labels':os.path.join(data_path,'lorelei/il8/en/labels.txt'),
    'train':os.path.join(data_path,'lorelei/il8/en/splits/train-8096.txt'),
    'dev':os.path.join(data_path,'lorelei/il8/en/splits/dev-172.txt'),
    'max_vocab':6000,
    'max_df':0.6    
}

wiki_shorts = {'en': wiki_shorts_en, 'zh': wiki_shorts_zh}
lorelei = {'ru': lorelei_ru}

dictionary_zh_en = os.path.join(data_path,'dictionary/cedict.txt')
dictionary_ru_en = os.path.join(data_path,'lorelei/il8/ru_en_dict.txt')

def read_text(file, num=False):
    """ Read from txt [file].
    If [num], then data is numerical data and will need to convert each
    string to an int.
    """
    with open(file,'r') as f:
        data = f.read().splitlines()
    if num:
        data = [int(i) for i in data]
    return data

def prepare_data(files, language, debug):
    print('\npreparing data')
    # parse files
    docs = read_text(files['docs'])
    labels = read_text(files['labels'], num=True)
    train = read_text(files['train'], num=True)
    dev = read_text(files['dev'], num=True)
    stopwords = read_text(stopword_files[language])

    if debug:
        max_vocab = 200
        max_df = 1.0
    else:
        max_vocab = files['max_vocab']
        max_df = files['max_df']

    # split data 
    docs_train = [docs[i] for i in train]
    docs_dev = [docs[i] for i in dev]

    labels_train = [labels[i] for i in train]
    labels_dev = [labels[i] for i in dev]

    # preprocess docs
    word_doc_train, word_doc_dev, word_doc_test, index, vocab = \
        vectorize(docs_train, stopwords, language, max_vocab, max_df, docs_dev)

    data = {}
    print('\nTrain size: {}'.format(word_doc_train.shape))
    data['word_doc_train'] = word_doc_train
    print('Dev size: {}'.format(word_doc_dev.shape))
    data['word_doc_dev'] = word_doc_dev
    data['labels_train'] = labels_train
    data['labels_dev'] = labels_dev
    print('Vocab size: {}'.format(len(index)))
    data['index'] = index
    data['vocab'] = vocab
    return data


def parse_dict(dict_file, separator='\t'):
    """ Parse [file] that contains a dictionary"""
    text = read_text(dict_file)
    dictionary = {}
    for entry in text:
        w2, w1 = tuple(entry.split(separator))
        dictionary[w1] = w2
    return dictionary


# Functions to get data #

def wiki_data(language1='en', language2='zh', debug=False):
    data1 = prepare_data(wiki_shorts['en'], language1, debug)
    data2 = prepare_data(wiki_shorts['zh'], language2, debug)
    return data1, data2

def lorelei_data(language='ru', debug=False):
    dataset = lorelei[language]
    data1 = prepare_data(dataset['en'], 'en', debug)
    data2 = prepare_data(dataset[language], language, debug)
    return data1, data2 


# After getting data, get dictionary #

def prepare_dictionary(index1, index2, dict_file=dictionary_ru_en):
    """
    Set up dictionaries for MTAnchor system.

    [Dictionary] must map words from [resource1.corpus.language] to 
    [resource2.corpus.language] for this function to work correctly.
    It sets up three kinds of dictionaries:

    1. [resource1.dictionary] contains dictionary entries for words  
    in [resource1.corpus.language]. This will be used for translating
    words on the interface.  Only will contain words in both corpora.

    2. [resource2.dictionary] contains dictionary entries for words  
    in [resource2.corpus.language]. This will be used for translating
    words on the interface. Only will contain words in both corpora.

    3. [dictionary] is a index-to-index mapping from language1
    to language2 where entries must contain words in both corpora. 
    This dictionary will be used for the topic model.
        
    """
    print('\npreparing dictionary')
    index_map = []
    dict1_2 = {}
    dict2_1 = {}

    if dict_file is not None:
        dict_parsed = parse_dict(dict_file)
            
        for w1, w2 in dict_parsed.items():
            if w1 in index1 and w2 in index2:
                i1 = index1[w1]
                i2 = index2[w2]
                index_map.append([i1, i2]) 


            if w1 in index1:
                dict1_2[w1] = w2
            if w2 in index2:
                dict2_1[w2] = w1

                
    dictionary = {}
    print('Dictionary size: {}'.format(len(index_map)))
    dictionary['index_map'] = index_map
    dictionary['dict1_2'] = dict1_2
    dictionary['dict2_1'] = dict2_1

    return dictionary 






