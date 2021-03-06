from interface import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    updates = db.relationship('Update', backref='user', lazy='dynamic')

class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anchors1 = db.Column(db.String)
    anchors2 = db.Column(db.String)
    topics1 = db.Column(db.String)
    topics2 = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Start(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anchors1 = db.Column(db.String)
    topics1 = db.Column(db.String)
    Q1 = db.Column(db.String)
    vocab1 = db.Column(db.String)    
    index1 = db.Column(db.String)
    dict1 = db.Column(db.String)
    anchors2 = db.Column(db.String)    
    topics2 = db.Column(db.String)    
    Q2 = db.Column(db.String)
    vocab2 = db.Column(db.String)    
    index2 = db.Column(db.String) 
    dict2 = db.Column(db.String)
 