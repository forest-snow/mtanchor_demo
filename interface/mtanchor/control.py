from . import data, utils, infer 
import anchor_topic.topics
import numpy
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score



DEBUG = False
language1 = 'en'
language2 = 'ru'
K = 10
SEED = 34
TOP = 15


def start():
    data1, data2 = data.lorelei_data(language2, DEBUG)
    dct = data.prepare_dictionary(data1['index'], data2['index'])

    A1, A2, Q1, Q2, anchors1, anchors2 = anchor_topic.topics.model_multi_topics(
        M1=data1['word_doc_train'], 
        M2=data2['word_doc_train'],
        k=K,
        threshold1=0.008,
        threshold2=0.01,
        dictionary=dct['index_map'],
        seed=SEED
    )


    start_data = {}
    start_data['words1'] = utils.get_top_topic_words(A1, TOP, data1['vocab'])
    start_data['anchors1'] = utils.convert_2dlist(anchors1, data1['vocab'])
    start_data['words2'] = utils.get_top_topic_words(A2, TOP, data2['vocab'])
    start_data['anchors2'] = utils.convert_2dlist(anchors2, data2['vocab'])
    start_data['Q1'] = Q1
    start_data['Q2'] = Q2
    start_data['vocab1'] = data1['vocab']
    start_data['vocab2'] = data2['vocab']
    start_data['index1'] = data1['index']
    start_data['index2'] = data2['index']
    start_data['dict1'] = dct['dict1_2']
    start_data['dict2'] = dct['dict2_1']
    start_data['M_dev1'] = data1['word_doc_dev']
    start_data['M_dev2'] = data2['word_doc_dev']
    start_data['Y_dev1'] = data1['labels_dev']
    start_data['Y_dev2'] = data2['labels_dev']

    scores = evaluate(A1, A2, start_data)
    start_data['intra1'] = scores['intra1']
    start_data['cross1'] = scores['cross1']
    start_data['intra2'] = scores['intra2']
    start_data['cross2'] = scores['cross2']

    return start_data


def update(anchors1, anchors2, data):
    anchor_nums1 = utils.convert_2dlist(anchors1, data['index1'])
    anchor_nums2 = utils.convert_2dlist(anchors2, data['index2'])

    A1 = anchor_topic.topics.update_topics(data['Q1'], anchor_nums1)
    A2 = anchor_topic.topics.update_topics(data['Q2'], anchor_nums2)

    scores = evaluate(A1, A2, data)

    data['topics1'] = utils.get_top_topic_words(A1, TOP, data['vocab1'])
    data['anchors1'] = anchors1
    data['topics2'] = utils.get_top_topic_words(A2, TOP, data['vocab2'])
    data['anchors2'] = anchors2
    data['intra1'] = scores['intra1']
    data['cross1'] = scores['cross1']
    data['intra2'] = scores['intra2']
    data['cross2'] = scores['cross2']

    return data

def infer_topics(word_doc, word_topic):
    """Infer topics for [word_doc], word distribution of documents,
     using [word_topic], word distribution of topics.

    """
    topic_word = word_topic.T
    return infer.variational_bayes(word_doc, topic_word)

def train_classifier(X, Y):
    clf = LinearSVC(class_weight = 'balanced', dual=False, random_state=SEED)
    clf.fit(X, Y)
    return clf

def score(label, prediction):
    score = f1_score(label, prediction, average='micro')
    return '{0:.2f}'.format(score*100)

def evaluate(A1, A2, data):
    # infer topics from word_doc
    X1 = infer_topics(data['M_dev1'], A1)
    X2 = infer_topics(data['M_dev2'], A2)
    clf1 = train_classifier(X1, data['Y_dev1'])
    clf2 = train_classifier(X2, data['Y_dev2'])

    scores = {}

    Y_intra1 = clf1.predict(X1)
    Y_cross1 = clf1.predict(X2)
    Y_intra2 = clf2.predict(X2)
    Y_cross2 = clf2.predict(X1)

    scores['intra1'] = score(data['Y_dev1'], Y_intra1)
    scores['cross1'] = score(data['Y_dev2'], Y_cross1)
    scores['intra2'] = score(data['Y_dev2'], Y_intra2)
    scores['cross2'] = score(data['Y_dev1'], Y_cross2)
    return scores 
