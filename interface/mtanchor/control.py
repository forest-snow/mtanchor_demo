from . import data, utils 
import anchor_topic.topics

DEBUG = True
language1 = 'en'
language2 = 'ru'
K = 5
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
        threshold2=0.008,
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


    return start_data

def update(anchors1, anchors2, data):
    anchor_nums1 = utils.convert_2dlist(anchors1, data['index1'])
    anchor_nums2 = utils.convert_2dlist(anchors2, data['index2'])

    A1 = anchor_topic.topics.update_topics(data['Q1'], anchor_nums1)
    A2 = anchor_topic.topics.update_topics(data['Q2'], anchor_nums2)


    data['topics1'] = utils.get_top_topic_words(A1, TOP, data['vocab1'])
    data['anchors1'] = anchors1
    data['topics2'] = utils.get_top_topic_words(A2, TOP, data['vocab2'])
    data['anchors2'] = anchors2

    return data

