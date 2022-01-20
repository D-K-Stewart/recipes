from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# from flask import Bcrypt
from flask_app.models.user import User
import re


# DATABASE = ''

class Recipe:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.instructions = db_data['instructions']
        self.under_min = db_data['under_min']
        self.date_made_on = db_data['date_made_on']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        

# ----------------------------------------------------------------C

    @classmethod # doesn't taget the instance but instead targets the class itself
    def create(cls,data):
        query = "INSERT INTO recipes (name, description, instructions, under_min, date_made_on, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_min)s, %(date_made_on)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL('recipes').query_db(query, data)
    
        # list of dictionaries

    # ---------------------------------------------------------------R

    @classmethod # doesn't taget the instance but instead targets the class itself
    def get_all(cls):
        query = "SELECT * FROM recipes"
        results = connectToMySQL('recipes').query_db(query)  #list of dictionaries
        
        print(results)
        if len(results):
            all_recipes = []
            for recipes in results:
                all_recipes.append(cls(recipes))
            return all_recipes



    @classmethod # doesn't taget the instance but instead targets the class itself
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under_min=%(under_min)s, date_made_on=%(date_made_on)s WHERE id=%(id)s;"
        return connectToMySQL('recipes').query_db(query, data)


    @classmethod # doesn't taget the instance but instead targets the class itself
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)  #list of dictionaries
        if not results:
            return results

        data = {
            **results[0]
        }
        return cls(data)
    

    @classmethod 
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id=%(id)s;"
        return connectToMySQL('recipes').query_db(query, data)



    @staticmethod
    def validate_recipe(recipe):
        is_valid = True # we assume this is true
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters.", 'error_recipe_name')
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Descriptionn must be at least 3 characters.", 'error_recipe_description')
            is_valid = False
        if len(recipe['instructions']) < 10:
            flash("Instructions must be at least 10 characters.", 'error_recipe_instructions')
            is_valid = False
        if len(recipe['date_made_on']) < 3:
            flash("Month Day Year must be given.", 'error_date')
            is_valid = False

        return is_valid