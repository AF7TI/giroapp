# giroapp

frontend for https://github.com/AF7TI/girotick. display latest ionosphere metrics for each station as datatable and render to .json for other stuff . Docker based on tiangolo uwsgi-nginx-flask-docker.

point app to your db via app.config['SQLALCHEMY_DATABASE_URI'] in [/app/main.py]

online at http://metrics.af7ti.com/ . http://metrics.af7ti.com/stations.json for raw data.


