from flask import render_template, request, session, redirect, url_for
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
        print(session['uid'])
        user = User.query.get(session['uid'])
        update = user.updates.order_by(Update.id.desc()).first()
        topics = convert.db_data_to_topics(update)

    except (KeyError, AttributeError):
        # no session has started or app falsely thought there was session
        
        # need to create user if not in database
        if 'uid' not in session:
            user = User()
            db.session.add(user)
            db.session.commit()

        else:

            user = User.query.get(session['uid'])
            if user is None:
                user = User()
                db.session.add(user)
                db.session.commit()


        session['uid'] = user.id

        start_data = Start.query.first()

        topics = convert.db_data_to_topics(start_data)

    print('rendering index\n\n')
    print(session['uid'])
    return render_template('index.html', topics=topics)


@app.route('/update', methods=['POST'])
def update():
    # retrieve anchors, update model, save new data in database before redirecting
    json_data = request.get_json()
    # need to get Q, vocab, and index from start_data
    start_data = Start.query.first()

    new_data = control.update(
            anchors1 = json_data['l1'], 
            anchors2 = json_data['l2'], 
            data = convert.start_data_to_control(start_data)
        )

    update = convert.data_to_update_obj(new_data, session['uid'])
    
    db.session.add(update)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/restart')
def restart():
    print('restarting')

    user = User.query.get(session['uid'])
    for update in user.updates:
        db.session.delete(update)

    db.session.delete(user)
    db.session.commit()
    session.clear()
    return redirect(url_for('index'))

@app.route('/finish')
def finish():
    print('submitting')
    session.clear()
    return render_template('finish.html')






