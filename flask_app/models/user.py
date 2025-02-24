# import the function that will return an instance of a connection
from flask_app.config.mysql_connection import connect_to_mysql
# model the class after the friend table from our database
from flask import render_template, redirect, request, session, flash
import re
# create a regular expression object that we'll use later   
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "plant_quiz" # This should be the schema name, not the table name!
    # For some reason the data keys MUST match the self.keys (ex: self.first_name & data["first_name"]) or else it wont work!)
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.date = data["date"]
        # must connect it to data if you want to be able to change it
        self.bio = data.get('bio', "None Yet.") 
        self.general_score = data.get('general_score', 0)
        self.pnw_score = data.get('pnw_score', 0)
        self.herb_score = data.get('herb_score', 0)
        self.flower_score = data.get('flower_score', 0)
        self.created_at = None
        self.updated_at = None


    @staticmethod
    def validate_email(user):
        is_valid = True
        # test whether a field matches the pattern
        if not email_regex.match(user['email']): 
            flash("Invalid email address!", category="box1")
            is_valid = False
        return is_valid
    
    @classmethod
    def same_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connect_to_mysql(cls.DB).query_db(query,data)
        print("Result of email is:", result)
        # Didn't find a matching user
        if len(result) < 1:
            print("Unique email")
            return False
        print("Email already in use!")
        flash("Email already in use!", category="box1")
        return True
    
    @staticmethod
    def validate_form(user):
        is_valid = True # we assume this is true
        if len(user['fname']) == 0:
            flash("First name can't be blank.", category="box1")
            is_valid = False
        elif len(user['fname']) < 2:
            flash("First name must be at least 2 characters.", category="box1")
            is_valid = False
        if len(user['lname']) == 0:
            flash("Last name can't be blank.", category="box1")
            is_valid = False
        elif len(user['lname']) < 2:
            flash("Last name must be at least 2 characters.", category="box1")
            is_valid = False
        if len(user['email']) == 0:
            flash("Email can't be blank.", category="box1")
            is_valid = False
        if len(user["pw"]) < 8:
            flash("Password must be at least 8 characters.", category="box1")
            is_valid = False
        if user["cpw"] != user["pw"]:
            flash("Passwords must match!", category="box1")
            is_valid = False
        return is_valid




    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connect_to_mysql function with the schema you are targeting.
        results = connect_to_mysql(cls.DB).query_db(query) # or connect_to_mysql(cls.DB)
        # Create an empty list to append our instances of friends
        all_users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            all_users.append(cls(user))
        return all_users
    
    # the get_one method will be used when we need to retrieve just one specific row of the table
    @classmethod
    def get_one(cls, user_id):
        print("Entered get_one method!")
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        print("Running query...")
        data = {'id': user_id}
        print("Adding data...")
        results = connect_to_mysql(cls.DB).query_db(query, data)
        if results:
            print("the results are:", results)
            return cls(results[0])
        else:
            print("Returning none!")
            return None
    
    @classmethod
    def save(cls, data ):
        query = """INSERT INTO users (first_name, last_name, email, date, password, created_at , updated_at)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), %(password)s, NOW(), NOW() );"""
        return connect_to_mysql(cls.DB).query_db(query,data)


    @classmethod
    def get_by_email(cls,data):
        print("Getting by email!")
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connect_to_mysql(cls.DB).query_db(query,data)
        print("result is:", result)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])


    # @classmethod
    # def delete(cls, user_id):
    #     query = """DELETE FROM users WHERE id = %(id)s;"""
    #     data = {'id': user_id}
    #     print("Deleting user...")
    #     results = connect_to_mysql(cls.DB).query_db(query,data)
    #     print("results:", results)
    #     return results
    

    @classmethod
    def edit_bio(cls, data):
        query = """Update users 
        SET  bio = %(bio)s, updated_at = NOW()
        WHERE id = %(user_id)s;"""
        return connect_to_mysql(cls.DB).query_db(query,data)
    

    @classmethod
    def edit_herb(cls, data):
        query = """Update users 
        SET herb_score = %(herb)s, updated_at = NOW()
        WHERE id = %(user_id)s;"""
        return connect_to_mysql(cls.DB).query_db(query,data)
    
    @classmethod
    def edit_flower(cls, data):
        query = """Update users 
        SET herb_flower = %(flower)s, updated_at = NOW()
        WHERE id = %(user_id)s;"""
        return connect_to_mysql(cls.DB).query_db(query,data)
    