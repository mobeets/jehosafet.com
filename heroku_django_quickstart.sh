mkdir DIRNAME
cd DIRNAME

virtualenv venv --distribute
source venv/bin/activate
pip install Django psycopg2 gunicorn dj-database-url

django-admin.py startproject APPNAME .
echo web: gunicorn APPNAME.wsgi > Procfile

foreman start
# Ctrl+C

pip freeze > requirements.txt
deactivate

# venv and *.pyc to .gitignore

# add dj_database_url to bottom of settings.py

git init
git add .
git commit -m "initial commit"

heroku create --stack cedar
heroku apps:rename APPNAME

git push heroku master
heroku open

# heroku run python manage.py syncdb
# heroku run python manage.py shell
