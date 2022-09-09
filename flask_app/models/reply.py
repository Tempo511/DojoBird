from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Reply:
    def __init__( self , data ):
        self.id = data['id']
        self.reply = data['reply']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.post_id = data['post_id']

    @classmethod
    def insert_reply( cls, new_reply ):
        query = "INSERT INTO twitter_clone.replies(reply, user_id, post_id) "
        query+= "VALUES(%(reply)s,%(user_id)s, %(post_id)s);"
        results = connectToMySQL('twitter_clone').query_db(query, new_reply)
        return results

    @classmethod
    def delete_reply( cls, reply):
        query= "DELETE FROM replies WHERE id = %(id)s;"
        results = connectToMySQL('twitter_clone').query_db(query, reply)
        return results

    @classmethod
    def update_reply(cls, reply):
        query = "UPDATE replies SET reply = %(reply)s, user_id = %(user_id)s, postid = %(post_id)s WHERE id = %(id)s;"
        return connectToMySQL('twitter_clone').query_db(query, reply)

    @classmethod
    def select_reply(cls, reply):
        query = "SELECT * FROM replies WHERE id = %(id)s;"
        results = connectToMySQL('twitter_clone').query_db(query, reply)

        if len(results) < 1:
            print("no match")
            return False
        return cls(results[0])

    @classmethod
    def select_all_replies(cls, reply):
        query = "SELECT * FROM replies WHERE post_id = %(post_id)s;"
        results = connectToMySQL('twitter_clone').query_db(query, reply)
        replies = []
        for reply in results:
            replies.append( cls(reply))
        return replies

    @classmethod
    def insert_reply_like( cls, new_like ):
        query = "INSERT INTO twitter_clone.reply_likes(reply_id, user_id, status) "
        query+= "VALUES(%(reply_id)s,%(user_id)s, %(status)s);"
        results = connectToMySQL('twitter_clone').query_db(query, new_like)
        return results

    @classmethod
    def remove_reply_like( cls, new_like ):
        query = "DELETE FROM twitter_clone.reply_likes WHERE user_id = %(user_id)s AND reply_id = %(reply_id)s;"
        results = connectToMySQL('twitter_clone').query_db(query, new_like)
        return results

    @classmethod
    def get_reply_with_likes(cls, data):
        query = "SELECT * FROM reply_likes WHERE reply_id = %(reply_id)s;"

        results = connectToMySQL('twitter_clone').query_db(query, data)

        likes_list = []

        if not results:
            return likes_list

        else: 
            for val in results:
                likes_list.append(val)

        return likes_list


    @classmethod
    def isLiked (cls, data):
        query = "SELECT * FROM reply_likes WHERE user_id = %(user_id)s AND reply_id = %(reply_id)s;"
        results = connectToMySQL('twitter_clone').query_db(query, data)
        if not results:
            print("nothing in likes ")
            return False
        else: 
            return True
        