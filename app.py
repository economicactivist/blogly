"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask.helpers import url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, db_connect, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "KJOJKLJKJLKJL"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug=True

debug = DebugToolbarExtension(app)

db_connect(app)
db.drop_all()
db.create_all()


@app.route('/')
def redirect_to_user_list():
    return redirect(url_for('list_users'))

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('user-list.html', users=users)

@app.route('/users/new')
def add_new_user():
    return render_template('new-user.html')

@app.route('/users/new', methods=['POST'])
def add_new_user_to_db():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["img_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    #####################
    return redirect(url_for('list_users'))

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    user = User.query.get_or_404(user_id)
    print(user.image_url)
    return render_template('user-detail.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    #maybe I should just pass user here
    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def post_user_edits_to_db(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["img_url"]
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('list_users'))

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    flash('User Deleted')
    user_id = int(user_id)
    User.query.filter_by(id=user_id).delete()
    return redirect(url_for('list_users'))

    #comment to update commit


 