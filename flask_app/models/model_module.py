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
        self.panel_finish = data['panel_finish']
        self.hp = data['hp']
        self.one_u = data['one_u']
        self.condition = data['condition']
        self.photo = data['photo']
        self.users_id = data['users_id']
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
        print(f"model_module: get_all results is {results}")
        return results

    @classmethod
    def add_module(cls, module_data):
        # print(f"model - add_module: module_data is: {module_data}")
        data = {
            'module_name': module_data['module_name'],
            'maker': module_data['maker'],
            'function': module_data['function'],
            'hp': module_data['hp'],
            'one_u': module_data['one_u'],
            'condition': module_data['condition'],
            'panel_finish': module_data['panel_finish'],
            'users_id': module_data['users_id'],
            'price': module_data['price'],
            'shipping': module_data['shipping'],
            'description': module_data['description']
        }
        query = """INSERT INTO modules (module_name, maker, `function`, panel_finish, hp, one_u, `condition`, users_id, price, shipping, `description` ) 
                   VALUES (%(module_name)s, %(maker)s, %(function)s, %(panel_finish)s, %(hp)s, %(one_u)s, %(condition)s, %(users_id)s, %(price)s, %(shipping)s, %(description)s)"""
        result = connectToMySQL(db).query_db(query, data)
        return result
    
    @classmethod
    def get_one(cls, module_id):
        print(f"get_one: module_id is {module_id}")
        module_id = {
            'module_id': module_id
        }
        query = """SELECT * FROM users JOIN modules
                    ON users.id = modules.users_id
                    WHERE modules.id = %(module_id)s;"""
        module = connectToMySQL(db).query_db(query, module_id)
        if not module:
            return False
        print(f"model - get_one: module = {module}")
        return module[0]# get module data in displayable format

    @classmethod
    def change_module(cls, data):
        print(f"model - Change_module: data is {data}")
        query = """UPDATE modules SET module_name = %(module_name)s, maker = %(maker)s, 
                    `function` = %(function)s, panel_finish = %(panel_finish)s, 
                    hp = %(hp)s, one_u = %(one_u)s, `condition` = %(condition)s, 
                    photo = %(photo)s,  price = %(price)s,
                    shipping = %(shipping)s, `description` = %(description)s
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

