# import the function that will return an instance of a connection
from flask_app.config.mysql_connection import connect_to_mysql
from flask import flash
import re
from flask_app.models import user
# create a regular expression object that we'll use later   
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Post:
    DB = "plant_quiz" # This should be the schema name, not the table name!
    # For some reason the data keys MUST match the self.keys (ex: self.first_name & data["first_name"]) or else it wont work!)
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.date = data['date']
        self.created_at = None
        self.updated_at = None
        self.user_id = data['user_id']
        self.creator = None
        self.comments = None


    @staticmethod
    def validate_post(post):
        is_valid = True # we assume this is true
        if len(post['title']) < 1:
            flash("Title cannot be blank.")
            is_valid = False
        if len(post['title']) > 45:
            flash("Title cannot exceed 45 characters.")
            is_valid = False
        if len(post['content']) < 1:
            flash("Content cannot be blank.")
            is_valid = False
        if len(post['content']) > 1000:
            flash("Content cannot exceed 1000 characters.")
            is_valid = False
        return is_valid

    @classmethod
    def save_post(cls, data ):
        print("Entered save post")
        query = """INSERT INTO posts (title, content, date, created_at, updated_at, user_id)
        VALUES (%(title)s, %(content)s, NOW(), NOW(), NOW(), %(user_id)s );"""
        print("Inserted values into posts")
        return connect_to_mysql(cls.DB).query_db(query,data)


    # Now we use class methods to query our database
    @classmethod
    def get_all_posts(cls):
        print("Entered get all posts")
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC;"
        # make sure to call the connect_to_mysql function with the schema you are targeting.
        results = connect_to_mysql(cls.DB).query_db(query) # or connect_to_mysql(cls.DB)
        print("Results are:", results)
        # Create an empty list to append our instances of Sightings
        all_posts = []
        # Iterate over the db results and create instances of Sightings with cls.
        for post in results:
            one_post=cls(post)
            # This dictionary MUST contain every column from users table or you will get errors! 
            one_posts_author_info = {
                "id": post["users.id"],
                "first_name": post['first_name'],
                "last_name": post['last_name'],
                "email": post['email'],
                "password": post['password'],
                "general_score": post["general_score"],
                "pnw_score": post["pnw_score"],
                "herb_score": post["herb_score"],
                "flower_score": post["flower_score"],
                "date": post["date"],
                "created_at": post['users.created_at'],
                "updated_at": post['users.updated_at']
            }
            author = user.User(one_posts_author_info)
            print("Created author")
            # Associating the Sighting class instance with the User class instance by adding data to the empty author attribute in the Sighting class
            one_post.author = author
            # Append the posts containing the associated User to the list of posts
            all_posts.append(one_post)
        print("All posts:", all_posts)
        return all_posts
    

    # this method gets all info on a sighting and their creator by joining the tables and iterating through the rows
    #  and returning the one whose id matches the sighting_id.
    @classmethod
    def get_info(cls, post_id):
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id;"
        data = {'id': post_id}
        # make sure to call the connect_to_mysql function with the schema you are targeting.
        results = connect_to_mysql(cls.DB).query_db(query) # or connect_to_mysql(cls.DB)
        print("Results are:", results)
        for post in results:
            one_post=cls(post)
            print ("one post:", one_post)
            if one_post.id == post_id:
                # This dictionary MUST contain every column from users table or you will get errors! 
                one_posts_author_info = {
                    "id": post["users.id"],
                    "first_name": post['first_name'],
                    "last_name": post['last_name'],
                    "email": post['email'],
                    "password": post['password'],
                    "created_at": post['users.created_at'],
                    "updated_at": post['users.updated_at']
                }
                author = user.User(one_posts_author_info)
                # Associating the Sighting class instance with the User class instance by adding data to the empty author attribute in the Sighting class
                one_post.creator = author
                # WE've found the post we're looking for. Now we save it to the variable called "the_post"
                the_post = one_post
        print("the post:",the_post)
        return the_post
    

    @classmethod
    def delete_post(cls, post_id):
        query = """DELETE FROM posts WHERE id = %(id)s;"""
        data = {'id': post_id}
        print("Deleting post...")
        results = connect_to_mysql(cls.DB).query_db(query,data)
        print("results:", results)
        return results

    
    # the get_one method will be used when we need to retrieve just one specific row of the table
    @classmethod
    def get_one(cls, post_id):
        print("Getting one post...")
        query  = "SELECT * FROM posts WHERE id = %(id)s;"
        data = {'id': post_id}
        results = connect_to_mysql(cls.DB).query_db(query, data)
        print("results:", results)
        print("cls results:", cls(results[0]))
        return cls(results[0])

    @classmethod
    def edit(cls, data ):
        query = """Update posts
        SET title = %(title)s, content = %(content)s, updated_at = NOW()
        WHERE id = %(post_id)s;"""
        return connect_to_mysql(cls.DB).query_db(query,data)
