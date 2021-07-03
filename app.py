"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask.helpers import url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, db_connect, User, Post

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
    image_url = request.form["img_url"] or None

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

@app.route('/users/<int:user_id>/posts/new')
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('create-post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_new_blog_post_to_db(user_id):
    #!is this line necesary?
    user = User.query.get_or_404(user_id)
   
    post_title = request.form["post_title"]
    post_content = request.form["post_content"]
    new_post = Post(title=post_title, content=post_content, user_id=user.id)

    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('show_user_detail', user_id = user.id))
    #! why can't i just pass user_id directly?
    #! Needs to be changed to post_id
    #comment to update commit

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post-detail.html', post=post)

@app.route('path')
def edit_post(foo):
    return render_template('expression')

@app.route('path')
def delete_post(post_id):
    flash('Post Deleted')
    post_id = int(post_id)
    post = Post.query.get_or_404(post_id)
    Post.query.filter_by(id=post_id).delete()
    return redirect(url_for('show_user_detail', user_id = post.user.id))


 