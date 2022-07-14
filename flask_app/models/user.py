from flask_bcrypt import Bcrypt    
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.__init__ import app
from flask import flash
from flask_app.models import post
import re


bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []
        self.replies = []

    @classmethod
    def insert_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL("twitter_clone").query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("twitter_clone").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM twitter_clone.users WHERE id = %(user_id)s;"
        result = connectToMySQL("twitter_clone").query_db(query,data)
        
        # Didn't find a matching user
        if len(result) < 1:
            print("no match")
            return False
        return cls(result[0])

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL("twitter_clone").query_db(query)

        # Create an empty list to append our instances of friends
        users = []
        
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user)) 
        
        return users


    @classmethod
    def insert_follower( cls, new_follower ):
        query = "INSERT INTO twitter_clone.followers(follower_id, followed_id) "
        query+= "VALUES(%(follower_id)s,%(followed_id)s);"
        results = connectToMySQL('twitter_clone').query_db(query, new_follower)
        return results

    @classmethod
    def remove_follower( cls, new_follower ):
        query = "DELETE FROM twitter_clone.followers "
        query+= "WHERE follower_id = %(follower_id)s AND followed_id = %(followed_id)s"
        results = connectToMySQL('twitter_clone').query_db(query, new_follower)
        return results

    

    @staticmethod
    def validate_user( user ):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'err_email')
            is_valid = False
        if User.get_by_email(user):
            flash("Username already in use", "err_username_match")
            is_valid=False
        if len(user['first_name']) < 2 or len(user['last_name']) < 2:
            flash("Name must be at least two letters.", "err_name")
            is_valid=False
        if not user["first_name"].isalpha() or not user['last_name'].isalpha():
            flash("Name must only contain letters.", "err_name_alpha")
        if len(user['password']) < 8:
            flash("Password must be at leat 8 characters long", "err_pw_length")
        if user['password'] != user['confirm_password']:
            flash('Passwords must match', 'err_pw_match')
            is_valid = False
        return is_valid

    @classmethod
    def get_user_with_posts(cls, data):
        query = "SELECT * FROM twitter_clone.users LEFT JOIN twitter_clone.posts "
        query += "ON twitter_clone.posts.user_id = twitter_clone.users.id WHERE twitter_clone.users.id = %(id)s;"

        results = connectToMySQL('twitter_clone').query_db(query, data)

        user = cls ( results[0] )

        for row_from_db in results:
            # Now we parse the recipe data to make instances of recipes and add them into our list.
            post_data = {
                "id" : row_from_db["posts.id"],
                "post" : row_from_db["location"],
                "user_id" : row_from_db["user_id"],
                "created_at" : row_from_db["posts.created_at"],
                "updated_at" : row_from_db["posts.updated_at"]
            }
            user.posts.append( post.Posts( post_data ) )
        return user

    @classmethod
    def get_posts_by_user(user):
        query = "SELECT * FROM posts WHERE user_id = %(id)s;"
        results = connectToMySQL('twitter_clone').query_db(query, user)

        user_posts = []

        for val in results:
            list_post = post.Post(val)
            user_posts.append(list_post)
        return user_posts



    @classmethod
    def get_followed(cls, data):
        query = "SELECT * FROM followers WHERE follower_id = %(follower_id)s;"

        results = connectToMySQL('twitter_clone').query_db(query, data)

        followed_list = []

        if not results:
            print("no results from followers")
            return followed_list

        else: 
            for val in results:
                user = User.get_by_id({"user_id" : val['followed_id']})
                followed_list.append(user)

        return followed_list

    @classmethod
    def isFollowed (cls, data):
        query = "SELECT * FROM followers WHERE follower_id = %(follower_id)s AND followed_id = %(followed_id)s;"
        results = connectToMySQL('twitter_clone').query_db(query, data)
        print(results)
        if not results:
            return False
        else: 
            return True

    @staticmethod
    def validate_session(id_session):
        if 'user_id' in id_session:
            return True
        else: return False

    
