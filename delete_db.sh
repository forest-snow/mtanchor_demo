#!/bin/bash
rm interface/app.db
rm -r migrations
flask db init
flask db migrate
flask db upgrade 
