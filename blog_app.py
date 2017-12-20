#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""a bloggin app"""

import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, render_template, flash


DATABASE = 'blog.db'
DEBUG = True
SECRET_KEY = '8\x00xqN\xbd\x85\xa6B<\x88\xc2c\xb4\xb84A\x02\x96\xd4\xe9\x0c\x03\x1c'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    """Connects to database"""
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    """creates the database for app"""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    """initializes connection to database"""
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    """ends connection to database"""
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def main_page():
    """main page of app"""
    cur1 = g.db.execute('SELECT published_date, title, author, content from POSTS ORDER BY published_date DESC')
    posts = [dict(pub_date=row[0], title=row[1],
                  author=row[2], content=row[3]) for row in cur1.fetchall()]
    return render_template('mainpage.html', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """allows uers to login"""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
        if request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password or password'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            flash('You have been logged in')
            return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error=error)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """loads the dashboard"""
    cur1 = g.db.execute('SELECT published_date, title, author, id, content from POSTS ORDER BY published_date DESC')
    posts = [dict(pub_date=row[0], title=row[1],
                  author=row[2], post_id=row[3], content=row[4]) for row in cur1.fetchall()]
    return render_template('dashboard.html', posts=posts)


@app.route('/post/add', methods=['GET', 'POST'])
def add_post():
    """adds a post"""
    if request.method == 'GET':
        return render_template('addpost.html')
    if request.method == 'POST':
        if not session.get('logged_in'):
            return redirect('/login')
        try:
            g.db.execute('INSERT INTO POSTS (published_date, title, author, content) VALUES (?,?,?,?)',
                         (request.form['published_date'].title(), request.form['title'].title(), request.form['author'].title(), request.form['post_text'].title()))
            g.db.commit()
            flash('Post was successfully added')
            return redirect('/dashboard')
        except:
            flash("Somthing went wrong! Post not added.")
            return redirect('/post/add')


@app.route('/post/delete/<post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    """delete a post"""
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        try:
            g.db.execute('DELETE FROM POSTS WHERE id = (?)', (post_id))
            g.db.commit()
            flash('Post was successfully deleted')
            return redirect('/dashboard')
        except:
            flash("Somthing went wrong! Post not deleted.")
            return redirect('/dashboard')


@app.route('/post/edit/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    """get post"""
    if request.method == 'GET':
        if not session.get('logged_in'):
            return redirect('/login')
        cur10 = g.db.execute('SELECT published_date, title, author, id, content from POSTS WHERE id = ?', (post_id,))
        change_post = [dict(date=row[0], title=row[1], author=row[2], post_id=row[3], content=row[4]) for row in cur10.fetchall()]
        return render_template('editpost.html', post_id=post_id, change_post=change_post)
    if request.method == 'POST':
        if not session.get('logged_in'):
            return redirect('/login')
        try:
            date = request.form['date']
            title = request.form['title']
            author = request.form['author']
            content = request.form['content']
            query = ('UPDATE POSTS SET published_date = ?, title = ?, author = ?, content = ? WHERE id =?')
            g.db.execute(query, (date, title, author, content, post_id))
            g.db.commit()
            return redirect('/dashboard')
        except:
            flash("Something went wrong! Post not changed.")
            return redirect('/post/edit/<post_id>')

@app.route('/logout')
def logout():
    """logs the user out"""
    session.pop('logged_in', None)
    return redirect('/')



if __name__ == '__main__':
    app.run()
