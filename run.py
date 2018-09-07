from interface import app, db
from interface.models import User, Update, Start



@app.shell_context_processor
def make_shell_context():
    print(db)
    return {'db': db, 'User': User, 'Update': Update, 'Start': Start}