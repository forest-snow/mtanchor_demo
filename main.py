from mtanchor.data import wiki_data, prepare_dictionary
from mtanchor.utils import convert_2dlist, get_top_topic_words
import anchor.topics 

DEBUG = True
language1 = 'en'
language2 = 'zh'
K=20
SEED=34
TOP = 15

data1, data2 = wiki_data(language1, language2, DEBUG)
dct = prepare_dictionary(data1['index'], data2['index'])

if __name__ == '__main__':
    A1, A2, Q1, Q2, anchors1, anchors2 = anchor.topics.model_multi_topics(
        M1=data1['word_doc_train'], 
        M2=data2['word_doc_train'],
        k=K,
        threshold1=0.008,
        threshold2=0.008,
        seed=SEED,
        dictionary=dct['index_map']
    )

    topic_words1 = get_top_topic_words(A1, TOP, data1['vocab'])
    anchor_words1 = convert_2dlist(anchors1, data1['vocab'])
    topic_words2 = get_top_topic_words(A2, TOP, data2['vocab'])
    anchor_words2 = convert_2dlist(anchors2, data2['vocab'])
