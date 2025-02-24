from flask_app.config.mysql_connection import connect_to_mysql
from flask_app import app
from flask_app.models import user
from flask import flash


class Comment:
    DB = 'plant_quiz'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.creator = None

    # Get comments
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM comments LEFT JOIN users ON comments.user_id = users.id;"
        results = connect_to_mysql(cls.DB).query_db(query)
        comments = []
        for post in results:
            comment = cls(post)
            user_data = {
                'id': post['users.id'],
                'first_name': post['first_name'],
                'last_name': post['last_name'],
                'email': post['email'],
                'password': post['password'],
                'general_score': post['general_score'],
                'pnw_score': post['pnw_score'],
                'herb_score': post['herb_score'],
                'flower_score': post['flower_score'],
                'date': post['date'],
                'created_at': post['users.created_at'],
                'updated_at': post['users.created_at']
            }
            comment.creator = user.User(user_data)
            comments.append(comment)
        return comments
    
    # post comment
    @classmethod
    def save_comment(cls, data):
        query = """INSERT INTO comments (content, date, created_at, updated_at, user_id, post_id)
            VALUES (%(content)s, NOW(), NOW(), NOW(), %(user_id)s, %(post_id)s)"""
        return connect_to_mysql(cls.DB).query_db(query, data)
    
    # validate comment
    @classmethod
    def validate(cls, data):
        is_valid = True
        if len(data['comment']) < 1:
            flash("Comment must not be blank", 'comment')
            is_valid = False
        return is_valid
    
    # delete comment
    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        return connect_to_mysql(cls.DB).query_db(query, data)
    
    # get all comments
    @classmethod
    def get_all(cls):
        print("Entered get all comments")
        query = "SELECT * FROM comments JOIN users ON comments.user_id = users.id ORDER BY comments.created_at ASC;"
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
        print("All comments:", all_posts)
        return all_posts
    
    
    # edit comment
    @classmethod
    def edit(cls, data):
        query = "UPDATE comments SET content = %(content)s, updated_at = NOW() WHERE id = %(id)s;"
        return connect_to_mysql(cls.DB).query_db(query, data)