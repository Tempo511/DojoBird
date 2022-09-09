from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import reply
from flask import flash


class Post:
    def __init__( self , data ):
        self.id = data['id']
        self.post = data['post']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.replies = []
        self.likes = []
    


    @classmethod
    def insert_post( cls, new_post ):
        query = "INSERT INTO twitter_clone.posts(post, user_id) "
        query+= "VALUES(%(post)s,%(user_id)s);"
        results = connectToMySQL('twitter_clone').query_db(query, new_post)
        return results

    @classmethod
    def delete_post( cls, post):
        query= "DELETE FROM twitter_clone.posts WHERE id = %(id)s;"
        results = connectToMySQL('twitter_clone').query_db(query, post)
        return results

    @classmethod
    def update_post(cls, post):
        query = "UPDATE twitter_clone.posts SET post = %(post)s, user_id = %(user_id)s WHERE id = %(id)s;"
        return connectToMySQL('twitter_clone').query_db(query, post)

    @classmethod
    def select_post(cls, post):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        results = connectToMySQL('twitter_clone').query_db(query, post)

        if len(results) < 1:
            print("no match")
            return False
        return cls(results[0])

    @classmethod
    def select_all_posts(cls):
        query = "SELECT * FROM twitter_clone.posts;"
        results = connectToMySQL('twitter_clone').query_db(query)

        posts = []
        
        for post in results:
            posts.append( cls(post)) 
        
        return posts

    @classmethod
    def get_post_with_replies(cls, data):
        query = "SELECT * FROM twitter_clone.replies WHERE post_id = %(id)s;"

        results = connectToMySQL('twitter_clone').query_db(query, data)

        print(results)

        reply_list = []

        for val in results:
            reply_list.append(reply.Reply(val))

        return reply_list


    @classmethod
    def get_post_with_likes(cls, data):
        query = "SELECT * FROM post_likes WHERE post_id = %(id)s;"

        results = connectToMySQL('twitter_clone').query_db(query, data)

        likes_list = []

        if not results:
            return likes_list

        else: 
            for val in results:
                likes_list.append(val)

        return likes_list

    @classmethod
    def get_posts_by_user(cls, user):
        query = "SELECT * FROM posts WHERE user_id = %(user_id)s;"
        results = connectToMySQL("twitter_clone").query_db(query, user)

        user_posts = []

        for row_from_db in results:
            post_data = {
                "id" : row_from_db["id"],
                "post" : row_from_db["post"],
                "user_id" : row_from_db["user_id"],
                "created_at" : row_from_db["created_at"],
                "updated_at" : row_from_db["updated_at"]
            }
            user_posts.append(cls(post_data))
        return user_posts

    @classmethod
    def insert_post_like( cls, new_like ):
        query = "INSERT INTO twitter_clone.post_likes(post_id, user_id, status) "
        query+= "VALUES(%(post_id)s,%(user_id)s, %(status)s);"
        results = connectToMySQL('twitter_clone').query_db(query, new_like)
        return results

    @classmethod
    def remove_post_like( cls, new_like ):
        query = "DELETE FROM twitter_clone.post_likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s;"
        results = connectToMySQL('twitter_clone').query_db(query, new_like)
        return results

    @classmethod
    def isLiked (cls, data):
        query = "SELECT * FROM post_likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s;"
        results = connectToMySQL('twitter_clone').query_db(query, data)
        print(results)
        if not results:
            return False
        else: 
            return True
        

    

    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['post']) < 1:
            is_valid = False
            flash("Must enter something", "err_post")
        return is_valid
    






