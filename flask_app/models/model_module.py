from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app

# from flask import flask_WTF
# from flask import flaskForm

db = "Eurorack_Junction"

class Module:
    def __init__(self, data):
        self.id = data['id']
        self.module_name = data['module_name']
        self.maker = data['maker']
        self.function = data['function']
        self.panel_finish = data['panel']
        self.hp = data['hp']
        self.one_u = data['one_u']
        self.condition = data['condition']
        self.photo = data['photo']
        self.owner = data['users_id']
        self.price = data['price']
        self.shipping = data['shipping']
        self.description = data['description']
    


    @staticmethod
    def validate_module(new_module):
        isValid = True
        if len(new_module['module_name']) < 2:
            flash("The module name must at least 2 characters", "module")
            isValid = False
        if len(new_module['maker']) < 1:
            flash("The maker must not be empty", "module")
            isValid = False
        if len(new_module['hp']) < 1:
            flash("The hp  must be at least 1", "module")
            isValid = False
        if len(new_module['price']) < 1:
            flash("The price must be at least 1$", "module")
        return isValid
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM users JOIN modules
                    ON users.id = modules.users_id;"""
        results = connectToMySQL(db).query_db(query)
        return results

    @classmethod
    def add_module(cls, module_data):
        
        data = {
            'module_name': module_data['module_name'],
            'maker': module_data['maker'],
            'function': module_data['function'],
            'panel_finish': module_data['panel_finish'],
            'hp': module_data['hp'],
            'condition': module_data['condition'],
            'photo': module_data['photo'],
            'owner': module_data['users_id'],
            'price': module_data['price'],
            'shipping': module_data['shipping'],
            'description': module_data['description']
        }
        query = """INSERT INTO modules (module_name, maker, function, panel_finish, hp, condition, photo, users_id, price, shipping, description ) 
                   VALUES (%(module_name)s, %(maker)s, %(function)s, %(panel_finish)s, %(hp)s, %(condition)s, %(photo)s, %(owner)s, %(price)s, %(shipping)s, %(description)s)"""
        result = connectToMySQL(db).query_db(query, data)
        return result
    
    @classmethod
    def get_one(cls, module_id):
        module_id = {
            'module_id': module_id
        }
        query = """SELECT * FROM users JOIN modules
                    ON users.id = modules.users_id
                    WHERE modules.id = %(module_id)s;"""
        module = connectToMySQL(db).query_db(query, module_id)
        if not module:
            return False
        return module# get module data in displayable format

    @classmethod
    def change_module(cls, data):
        query = """UPDATE modules SET module_name = %(module_name)s, maker = %(maker)s, 
                    function = %(function)s, panel_finish = %(panel_finish)s, 
                    hp = %(hp)s, one_u = %(one_u)s, condition = %(condition)s, 
                    photo = %(photo)s, user_id = %(user_id)s, price = %(price)s,
                    shipping = %(shipping)s, description = %(description)s
                    WHERE id = %(module_id)s"""
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False
        return True
    
    @classmethod
    def delete_module(cls, data):
        query =  """DELETE FROM modules WHERE id = %(module_id)s"""
        result = connectToMySQL(db).query_db(query, data)
        return result

