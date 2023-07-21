from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app

db = "Recipe_schema"

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']


    @staticmethod
    def validate_recipe(new_recipe):
        isValid = True
        print(f"in valide_recipe: new_recipe is: {new_recipe}")
        if len(new_recipe['recipe_name']) < 3:
            flash("The recipe name must at least 3 characters", "recipe")
            isValid = False
        if len(new_recipe['description']) < 3:
            flash("The description must not be empty", "recipe")
            isValid = False
        if len(new_recipe['instructions']) < 3:
            flash("The Instructions must not be empty", "recipe")
            isValid = False
        if len(new_recipe['date_made']) < 1:
            flash("Date made value must be provided", "recipe")
        return isValid
    
    @classmethod
    def get_all(cls):
        query = """SELECT recipes.name AS name, under30, first_name, recipes.id AS recipe_id
                    FROM users JOIN recipes
                    ON users.id = recipes.users_id;"""
        results = connectToMySQL(db).query_db(query)
        return results

    @classmethod
    def add_recipe(cls, recipe_data):
        under30 = 0
        if recipe_data['under30'] == "on":
            under30 = 1;
        data = {
            'name': recipe_data['recipe_name'],
            'description': recipe_data['description'],
            'instructions': recipe_data['instructions'],
            'under30': under30,
            'date_made': recipe_data['date_made'],
            'users_id': recipe_data['users_id']
        }
        query = """INSERT INTO recipes (name, description, instructions, under30, date_made, users_id ) 
                   VALUES (%(name)s, %(description)s, %(instructions)s, %(under30)s, %(date_made)s, %(users_id)s)"""
        result = connectToMySQL(db).query_db(query, data)
        return result
    
    @classmethod
    def get_one(cls, recipe_id):
        recipe_id = {
            'recipe_id': recipe_id
        }
        query = """SELECT recipes.name AS name, description, instructions, under30, first_name, recipes.id AS recipe_id, date_made
                    FROM users JOIN recipes
                    ON users.id = recipes.users_id
                    WHERE recipes.id = %(recipe_id)s;"""
        recipe = connectToMySQL(db).query_db(query, recipe_id)
        if not recipe:
            return False
        # get recipe data in displayable format
        recipe[0]['raw_date_made'] = recipe[0]['date_made']
        recipe[0]['date_made'] = recipe[0]['date_made'].strftime("%B %d %Y")
        if recipe[0]['under30'] > 0:
            recipe[0]['under30'] = "Yes"
        else:
            recipe[0]['under30'] = "No"
        return recipe[0]

    @classmethod
    def change_recipe(cls, data):
        query = """UPDATE recipes SET name = %(name)s, under30 = %(under30)s, 
                    description = %(description)s, instructions = %(instructions)s, 
                    date_made = %(date_made)s WHERE id = %(recipe_id)s"""
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False
        return True
    
    @classmethod
    def delete_recipe(cls, data):
        query =  """DELETE FROM recipes WHERE id = %(recipe_id)s"""
        result = connectToMySQL(db).query_db(query, data)
        return result

