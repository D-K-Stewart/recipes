from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def fullname(self):
        return f"{self.first_name} {self.last_name}"
    

    @classmethod
    def create(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s %(password)s)'
        new_users_id = connectToMySQL("recipes").query_db(query, data)

        return new_users_id



    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        return connectToMySQL("recipes").query_db(query, data)


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("recipes").query_db(query,data)
        # Didn't find a matching data
        if not results:
            return results
        return cls(results[0])


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("recipes").query_db(query,data)
        # Didn't find a matching data
        if len(result) < 1:
            return False
        return cls(result[0])


    @staticmethod
    def validate_user(data):
        is_valid = True # we assume this is true
        if len(data['first_name']) < 3:
            flash(u"Name must be at least 2 characters.", "create")
            is_valid = False
        if len(data['last_name']) < 3:
            flash(u"Name must be at least 2 characters.", "create")
            is_valid = False
        if len(data['email']) == 0:
            flash(u"Enter valid email.", "create")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash(u"Invalid email address", "create")
            is_valid = False
        if len(data['password']) < 3:
            flash(u"Password must be at least 3 characters.", "create")
            is_valid = False
        if data['confirm_password'] == ['password']:
            flash(u"Passwords do not match.", "create")
            is_valid = False
        return is_valid