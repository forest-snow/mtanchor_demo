import flask
from interface import app, db
from interface.mtanchor import control
from interface.models import User, Update, Start
import interface.convert as convert
import time



@app.route('/')
def index():
    # if first time, create new user and store starting data
    # else, retrieve anchors and top topic words from latest update
    if len(Start.query.all())==0: 
        print('getting initial data \n\n')
        start_data = control.start()
        s = convert.data_to_start_obj(start_data)
        db.session.add(s)
        db.session.commit()

    try:    
        # already have session
        user = User.query.get(flask.session['uid'])
        update = user.updates.order_by(Update.id.desc()).first()
        topics = convert.db_data_to_topics(update)
        scores = convert.db_data_to_scores(update)

    except(KeyError, AttributeError):
        # no session has started or app falsely thought there was session
        
        # need to create user if not in database
        if 'uid' not in flask.session:
            user = User()
            db.session.add(user)
            db.session.commit()

        else:
            user = User.query.get(flask.session['uid'])
            if user is None:
                user = User()
                db.session.add(user)
                db.session.commit()


        flask.session['uid'] = user.id

        start_data = Start.query.first()

        topics = convert.db_data_to_topics(start_data)
        scores = convert.db_data_to_scores(start_data)

    return flask.render_template('index.html', topics=topics, scores=scores)


@app.route('/update', methods=['POST'])
def update():
    # retrieve anchors, update model, save new data in database before redirecting
    json_data = flask.request.get_json()
    # need to get Q, vocab, and index from start_data
    start_data = Start.query.first()

    new_data = control.update(
            anchors1 = json_data['l1'], 
            anchors2 = json_data['l2'], 
            data = convert.start_data_to_control(start_data)
        )

    update = convert.data_to_update_obj(new_data, flask.session['uid'])
    
    db.session.add(update)
    db.session.commit()
    return "success"


@app.route('/restart')
def restart():
    print('restarting')

    user = User.query.get(flask.session['uid'])
    for update in user.updates:
        db.session.delete(update)

    db.session.delete(user)
    db.session.commit()
    flask.session.clear()
    return flask.redirect(flask.url_for('index'))

@app.route('/finish')
def finish():
    print('submitting')
    flask.session.clear()
    return flask.render_template('finish.html')


@app.route('/translate')
def translate():
    print('translating')
    text = flask.request.args.get('text')
    in_corpus = flask.request.args.get('in_corpus') == 'true'
    start_data = Start.query.first()
    dict1, dict2 = convert.start_data_to_dicts(start_data)
    vocab1, vocab2 = convert.start_data_to_vocab(start_data)
    if text in dict1:
        translation = dict1[text]
        if in_corpus and translation not in vocab2:
            translation = 'N/A'
    elif text in dict2:
        translation = dict2[text]
        if in_corpus and translation not in vocab1:
            translation = 'N/A'
    else:
        translation = 'N/A'
    return flask.jsonify(translation=translation)

@app.route('/autocomplete')
def autocomplete():
    start_data = Start.query.first()
    vocab1, vocab2 = convert.start_data_to_vocab(start_data)
    query = flask.request.args.get('query')
    suggestions = []
    for word in vocab1:
        if word.startswith(query):
            suggestions.append({'label':word, 'language':'l1'})

    for word in vocab2:   
        if word.startswith(query):
            suggestions.append({'label':word, 'language':'l2'})

    limit = min(len(suggestions), 8)
    choices = suggestions[:limit]
    return flask.jsonify(choices=choices)


@app.route('/uid')
def get_uid():
    return flask.jsonify(uid=flask.session['uid'])







