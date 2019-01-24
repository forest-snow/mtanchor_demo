from interface import app, db
from interface.convert import json_to_numpy
from interface.models import User, Update, Start
from interface.mtanchor import control, data
import sys
import csv

SEED = 34

def classify(anchors1, anchors2, topic_data):

    new_topic_data = control.update(anchors1, anchors2, topic_data)
    scores = {}
    scores['intra1'] = new_topic_data['intra1']
    scores['intra2'] = new_topic_data['intra2']
    scores['cross1'] = new_topic_data['cross1']
    scores['cross2'] = new_topic_data['cross2']
    return scores

def preprocess(entry):
    topics = entry.split('\n')
    anchors = []
    for topic in topics:
        anchors.append(topic.split(' '))
    return anchors

def get_data():
    data1, data2 = data.lorelei_data('ru', False, 'test')

    topic_data = {}
    topic_data['Q1'] = json_to_numpy(Start.query.first().Q1)
    topic_data['Q2'] = json_to_numpy(Start.query.first().Q2)
    topic_data['index1'] = data1['index']
    topic_data['index2'] = data2['index']
    topic_data['vocab1'] = data1['vocab']
    topic_data['vocab2'] = data1['vocab']
    topic_data['M_dev1'] = data1['word_doc_dev']
    topic_data['M_dev2'] = data2['word_doc_dev']
    topic_data['Y_dev1'] = data1['labels_dev']
    topic_data['Y_dev2'] = data2['labels_dev']
    return topic_data

if __name__ == '__main__':


    topic_data = get_data()
    
    uid = int(sys.argv[1])
    user = User.query.get(uid)
    start = Start.query.first()
    updates = user.updates.all()


    all_scores = []
    for update in updates:
        anchors1 = preprocess(update.anchors1)
        anchors2 = preprocess(update.anchors2)
        scores = classify(anchors1, anchors2, topic_data)
        time = (update.time - user.time).seconds
        scores['time'] = time
        all_scores.append(scores)

    with open('results/user'+'_'+str(uid)+'.csv', 'w') as f:
        fieldnames = ['time', 'intra1', 'cross1', 'intra2', 'cross2']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for scores in all_scores:
            writer.writerow(scores)

    