mkdir DIRNAME
cd DIRNAME

virtualenv --no-site-packages venv
source venv/bin/activate
pip install cherrypy

# create app.py
python app.py

pip freeze > requirements.txt
echo web: python app.py > Procfile

deactivate

git init
git add .
git commit -m "initial commit"

heroku create --stack cedar
heroku apps:rename APPNAME

git push heroku master
heroku open

foreman start
# go to 0.0.0.0:5000/
# Ctrl + c

# setting up postgres:
# https://devcenter.heroku.com/articles/heroku-postgresql#connection-in-python

heroku addons | grep POSTGRES
heroku addons:add heroku-postgresql:dev
# Added heroku-postgresql:dev to thu-jehosafet (Free).
# Attached as HEROKU_POSTGRESQL_AQUA_URL Database has been created and is available !
# This database is empty.
# If upgrading, you can transfer ! data from another database with pgbackups:restore.

heroku config | grep HEROKU_POSTGRESQL
heroku pg:promote HEROKU_POSTGRESQL_AQUA_URL
# remote connection with database
heroku pg:psql

###############################
# Local set up
###############################
sudo pip install -r requirements.txt
psql
># CREATE DATABASE test;
># \q

###############################
# setting up staging branch
###############################
heroku create --remote staging
# will need to change "fathomless-ocean-5751" below:
heroku apps:rename my-staging-app --app fathomless-ocean-5751
heroku addons:add heroku-postgresql:dev --app my-staging-app
heroku config --app my-staging-app | grep HEROKU_POSTGRESQL
# may need to change "AQUA" below:
heroku pg:promote HEROKU_POSTGRESQL_AQUA_URL --app my-staging-app
