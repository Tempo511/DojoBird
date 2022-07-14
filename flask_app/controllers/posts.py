
import re
from flask_app import app
from flask import render_template, request, redirect, session, flash, jsonify
from flask_app.models.user import User
from datetime import datetime
from flask_app.models.post import Post



@app.route('/post/new', methods=['POST'])
def create_post():
    if not Post.validate_post(request.form):
        return redirect('/dashboard')
    new_post = { 'post' : request.form['post'],
    'user_id' : session['user_id'],
    }
    results = Post.insert_post(new_post)
    return redirect('/dashboard')

@app.route('/post/<int:id>/edit')
def edit_post(id):
    post = Post.select_post({'id' : id})
    return render_template('edit_post.html', post = post)

@app.route('/post/<int:id>/delete')
def delete_post(id):
    Post.delete_post({'id': id})
    return redirect('/dashboard')

@app.route('/profile/<int:id>/delete')
def delete_post_from_profile(id):
    profile_post = Post.select_post({'id' : id})
    Post.delete_post({'id': id})
    return redirect(f'/profile/{profile_post.user_id}')


@app.route('/post/<int:id>/update', methods = ["POST"])
def update_post(id):
    Post.update_post({'id': id,
    "user_id" : session['user_id'],
    "post" : request.form['updated_post']})
    return redirect('/dashboard')



@app.route('/post/like/<int:id>')
def post_like(id):
    print(id)
    Post.insert_post_like({'post_id' : id,
    'user_id' : session['user_id'], 'status' : 1},)
    return jsonify(message="button liked")

@app.route('/post/unlike/<int:id>')
def post_unlike(id):
    data = {
        'user_id' : session['user_id'],
        'post_id' : id
    }
    Post.remove_post_like(data)
    return jsonify(message="button unliked")

