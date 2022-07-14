from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template, request, redirect, session, flash, jsonify
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models import post
from flask_app.models.reply import Reply
from datetime import datetime

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/user/login', methods=['POST'])
def login():
    # see if the username provided exists in the database

    data = { "email" : request.form["login_email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email", 'err_user_invalid')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['login_password']):
        # if we get False after checking the password
        flash("Invalid Password", "err_password_invalid")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/user/register', methods=['POST'])
def register_user():
    # validate the form here ...
    if not User.validate_user(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    # put the pw_hash into the data dictionary
    data = {
        "email": request.form['email'],
        "password" : pw_hash,
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name']
    }
    # Call the save @classmethod on User!   
    user_id = User.insert_user(data)
    print(user_id)

    # store user id into session
    session['user_id'] = user_id
    return redirect("/dashboard")


@app.route('/dashboard')
def dashboard():
    if User.validate_session(session):
        dash_user = User.get_by_id(session)
        print("user", dash_user)
        dash_posts= Post.select_all_posts()

        dash_posts.reverse()

        week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        return render_template('dashboard.html', dash_user = dash_user, dash_posts = dash_posts, User = User, Post = Post, datetime=datetime, week = week)
    else: return redirect('/')


@app.route('/timeline')
def timeline():
    if User.validate_session(session):

        follow_list = User.get_followed({'follower_id' : session["user_id"]})
        dash_user = User.get_by_id(session)
        timeline_posts = []
        for followed in follow_list:
            posts = Post.get_posts_by_user({"user_id" : followed.id})
            for val in posts:
                timeline_posts.append(val)
        timeline_posts = sorted(timeline_posts, key=lambda x: x.created_at, reverse=True)
        return render_template('mytimeline.html', follow_list = follow_list, dash_user = dash_user, timeline_posts = timeline_posts, Post = Post, User = User)
    else: return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/users')
def users():
    users = User.get_all_users()


    return render_template('users.html', users = users, User = User)

@app.route('/profile/<int:id>')
def profile_page(id):
    user = User.get_by_id({"user_id" : id}) 
    posts = Post.get_posts_by_user({"user_id" : id})   
    return render_template('profile_page.html', user = user, posts = posts)

@app.route('/user/follow/<int:id>')
def add_follower(id):
    data = {
        'follower_id' : session['user_id'],
        'followed_id' : id
    }
    User.insert_follower(data)
    return jsonify(message="button liked")

@app.route('/user/unfollow/<int:id>')
def remove_follower(id):
    data = {
        'follower_id' : session['user_id'],
        'followed_id' : id
    }
    User.remove_follower(data)
    return jsonify(message="button liked")




