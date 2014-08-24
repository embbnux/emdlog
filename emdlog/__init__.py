# welcome to my blog : Blog of Embbnux 
# url:http://www.embbnux.com/ 
# author : Embbnux Ji

# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# create our little application
app = Flask(__name__)
app.config.from_object('emdlog.config.Development')
#app.config.from_object('emdlog.config.Development')

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()
	g.db.close()

import emdlog.views

if __name__ == '__main__':
	app.run()
