import numpy
import json
from interface.models import User, Update, Start

def combine_to_topics(data):
    topics = []
    zipped_data = zip(data['words1'], data['anchors1'], data['words2'], data['anchors2'])
    for w1, a1, w2, a2 in zipped_data:
        topic = {
            'words1': w1,
            'anchors1': a1,
            'words2': w2,
            'anchors2': a2
        }
        topics.append(topic)

    return topics 


def list2d_to_string(array):
    string_list = []
    for row in array:
        string = ' '.join(row)
        string_list.append(string)

    return '\n'.join(string_list)

def string_to_list2d(string):
    list2d = []
    list1d = string.split('\n') 
    for row in list1d:
        new_row = row.split()
        list2d.append(new_row)

    return list2d

def to_json(obj):
    # obj is either list or dict
    j = json.dumps(obj)
    return j

def from_json(j):
    obj = json.loads(j)
    return obj

def numpy_to_json(array):
    l = array.tolist()
    return to_json(l)

def json_to_numpy(j):
    l = from_json(j)
    a = numpy.array(l)
    return a

def data_to_start_obj(start_data):
    s = Start(
        anchors1 = list2d_to_string(start_data['anchors1']),
        topics1 = list2d_to_string(start_data['words1']),
        Q1 = numpy_to_json(start_data['Q1']),
        vocab1 = to_json(start_data['vocab1']),
        index1 = to_json(start_data['index1']),
        dict1 = to_json(start_data['dict1']),
        anchors2 = list2d_to_string(start_data['anchors2']),
        topics2 = list2d_to_string(start_data['words2']),
        Q2 = numpy_to_json(start_data['Q2']),
        vocab2 = to_json(start_data['vocab2']),
        index2 = to_json(start_data['index2']),
        dict2 = to_json(start_data['dict2'])
    )

    return s

def db_data_to_topics(db_data):
    topics = []
    zipped_data = zip(
        string_to_list2d(db_data.topics1),
        string_to_list2d(db_data.anchors1),
        string_to_list2d(db_data.topics2),
        string_to_list2d(db_data.anchors2)
        )
    for w1, a1, w2, a2 in zipped_data:
        topic = {
            'words1': w1,
            'anchors1': a1,
            'words2': w2,
            'anchors2': a2
        }
        topics.append(topic)

    return topics 

def start_data_to_control(start_data):
    data = {}
    data['vocab1'] = from_json(start_data.vocab1) 
    data['vocab2'] = from_json(start_data.vocab2) 
    data['index1'] = from_json(start_data.index1) 
    data['index2'] = from_json(start_data.index2) 
    data['Q1'] = json_to_numpy(start_data.Q1)
    data['Q2'] = json_to_numpy(start_data.Q2)
    return data

def data_to_update_obj(data, uid):
    u = Update(
        user_id = uid,
        anchors1 = list2d_to_string(data['anchors1']), 
        topics1 = list2d_to_string(data['topics1']), 
        anchors2 = list2d_to_string(data['anchors2']), 
        topics2 = list2d_to_string(data['topics2'])
    )
    return u

def start_data_to_dicts(start_data):
    dict1 = from_json(start_data.dict1)
    dict2 = from_json(start_data.dict2)
    return dict1, dict2 

def start_data_to_vocab(start_data):
    vocab1 = from_json(start_data.vocab1)
    vocab2 = from_json(start_data.vocab2)
    return vocab1, vocab2


