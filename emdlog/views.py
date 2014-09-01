# welcome to my blog : Blog of Embbnux 
# url:http://www.embbnux.com/ 
# author : Embbnux Ji

# all the imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from emdlog import app
import re

@app.route('/')
def show_entries():
	cur = g.db.execute('select id, title, text from entries order by id desc')
	entries = [dict(id=row[0],title=row[1], text=row[2]) for row in cur.fetchall()]
	for entry in entries:
		if(len(entry['text'])>20):
			entry['text'] = entry['text'][0:19]
	return render_template('show_entries.html', entries=entries)

@app.route('/node/<int:node_id>')
def show_node(node_id):
	cur = g.db.execute('select id,title,text from entries where id= ? ',[node_id])
	node = [dict(id=row[0],title=row[1], text=row[2]) for row in cur.fetchall()]
	r = re.compile('<br>')
	text= r.sub('/r/n',node[0]['text'])
	node[0]['text']= text
	return render_template('show_node.html',node=node[0])

@app.route('/add', methods=['GET','POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	if request.method == 'POST':
		text= request.form['text']
		g.db.execute('insert into entries (title, text) values (?, ?)',
				[request.form['title'], text])
		g.db.commit()

		flash('New entry was successfully posted')
		return redirect(url_for('show_entries'))
	elif request.method == 'GET':
		return render_template('add_node.html')
	return redirect(url_for('show_entries'))

@app.route('/edit/<int:node_id>',methods=['GET'])
def edit_entry(node_id):
	if not session.get('logged_in'):
		abort(401)
	if request.method == 'GET':
		cur = g.db.execute('select id,title,text from entries where id= ? ',
				[node_id])
		node = [dict(id=row[0],title=row[1], text=row[2]) for row in cur.fetchall()]
		return render_template('edit_node.html',node=node[0])			
	return redirect(url_for('show_entries'))

@app.route('/save',methods=['POST'])
def save_entry():
	if not session.get('logged_in'):
		abort(401)
	if request.method == 'POST':
		text = request.form['text']
                title = request.form['title']
		node_id = request.form['node_id']
		g.db.execute('update entries set title= ? , text=? where id=?',
				[title,text,node_id])
		g.db.commit()

		flash('The article has been updated.')
		return redirect(url_for('show_node',node_id=node_id))
	return redirect(url_for('show_entries'))

@app.route('/delete',methods=['POST'])
def delete_entry():
	if not session.get('logged_in'):
		abort(401)
	node_id = request.args.get('node_id','')
	g.db.execute('delete from entries where id = ?',node_id)
	g.db.commit()
	flash('The article has been deleted')
	return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

