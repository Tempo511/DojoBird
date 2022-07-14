
import re
from unittest import removeResult
from flask_app import app
from flask import render_template, request, redirect, session, flash, jsonify
from flask_app.models.user import User
from datetime import datetime
from flask_app.models.post import Post
from flask_app.models.reply import Reply

@app.route('/post/<int:id>')
def reply_to_post(id):
    post = Post.select_post({'id' : id})
    replies = Reply.select_all_replies({'post_id' :id})
    reply_user = User.get_by_id(session)
    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return render_template('reply.html', post = post, replies = replies, user = reply_user, User = User, Reply = Reply, week=week, Post = Post) 

@app.route("/post/<int:id>/reply", methods=["post"])
def post_reply(id):
    new_reply = {
        'reply' : request.form['reply'],
        'user_id' : session['user_id'],
        'post_id' : id
    }
    Reply.insert_reply(new_reply)
    return redirect(f'/post/{id}')

@app.route('/reply/<int:post_id>/<int:reply_id>/delete')
def edit_reply(post_id, reply_id):
    Reply.delete_reply({'id' : reply_id})
    return redirect(f'/post/{post_id}')

@app.route("/reply/like/<int:id>")
def like_reply(id):
    print("made it!! ***********")
    Reply.insert_reply_like({'reply_id' : id,
    'user_id' : session['user_id'], 'status' : 1})
    return jsonify(message="button liked")

@app.route('/reply/unlike/<int:id>')
def unlike_reply(id):
    Reply.remove_reply_like({'reply_id' : id,
    'user_id' : session['user_id'], 'status' : 1})
    return jsonify(message="button unliked")


