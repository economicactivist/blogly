"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask.helpers import url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, db_connect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "KJOJKLJKJLKJL"

debug = DebugToolbarExtension(app)

db_connect(app)
db.create_all()


@app.route('/')
def redirect_to_user_list():
    return redirect(url_for('list_users'))

@app.route('/users')
def list_users():
    return render_template('user-list.html')

@app.route('users/new')
def add_new_user():
    return render_template('new-user.html')

@app.route('users/new', methods=['POST'])
def add_new_user_to_db():
    #####################
    return redirect(url_for('list_users'))

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    return render_template(url_for('user-detail.html', user_id=user_id))

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    return render_template(url_for('edit-user.html'))

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def post_user_edits_to_db(user_id):
    return redirect(url_for('list_users'))

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    flash('User Deleted')
    return redirect(url_for('list_users'))


 