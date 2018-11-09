#!/bin/bash
rm interface/app.db
rm -r migrations
export FLASK_APP=run.py
flask db init
flask db migrate
flask db upgrade 
