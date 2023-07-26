from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.model_module import Module
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
# from flask import Flaskform
# from flask import FileField 
import os
import uuid

    

UPLOAD_FOLDER = '../static/images/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/marketplace")
def modules():
    if 'user_id' not in session:
        session.clear()
        return render_template("/")
    all_modules = []
    modules = Module.get_all()
    for module in modules:
        a_module = {
            'module_id': module['id'],
            'module_name': module['module_name'],
            'maker': module['maker'],
            'function': module['function'],
            'panel_finish': module['panel_finish'],
            'hp': module['hp'],
            'one_u': module['one_u'],
            'condition': module['condition'],
            'photo': module['photo'],
            'owner': module['users_id'],
            'price': module['price'],
            'description': module['description']
        }
        all_modules.append(a_module)
    return render_template('modules.html', all_modules = all_modules)



@app.route("/modules/post_module")
def post_module():
    module = {
        'module_name': '',
        'maker': '',
        'function': '',
        'panel_finish': '',
        'hp': '',
        'one_u': False,
        'condition': '',
        'photo': '',
        'owner': session['user_id'],
        'price': 0,
        'shipping': 0,
        'description': ''
    }
    return render_template("new_module.html", module = module)

@app.route("/modules/add_module", methods=["POST"])
def add_module():
    if 'user_id' not in session:
        return redirect("/logout")
    valid = module.validate_module(request.form)
    if valid:
        module.add_module(request.form)
        return redirect("/modules")
    module = {
            'module_id': module['id'],
            'module_name': module['module_name'],
            'maker': module['maker'],
            'function': module['function'],
            'panel_finish': module['panel_finish'],
            'hp': module['hp'],
            'one_u': module['one_u'],
            'condition': module['condition'],
            'photo': module['photo'],
            'owner': module['users_id'],
            'price': module['price'],
            'shipping': module['shipping'],
            'description': module['description']
    }
    return render_template("new_module.html", module = module)

    return redirect("/modules")

@app.route("/modules/get_one/<int:module_id>")
def get_one(module_id):
    module = module.get_one(module_id)
    if not module:
        return redirect("/modules")
    return render_template("display_module.html", module = module)

@app.route("/modules/edit_module/<int:module_id>")
def edit_module(module_id):
    if 'user_id' not in session:
        redirect("/")
    module = module.get_one(module_id)
    if not module:
        return redirect("/modules")
    return render_template("edit_module.html", module = module)
    
@app.route("/modules/update_module", methods=['POST'])
def change_module():
    valid = Module.validate_module(request.form)
    if not valid:
        return render_template("edit_module.html", module = request.form )
    result = Module.change_order(request.form)
    return redirect("/modules")

@app.route("/modules/delete/<int:module_id>")
def delete_module(module_id):
    module_id = {
        'module_id': module_id
    }
    Module.delete_module(module_id)
    return redirect("/modules")

@app.route("/upload", methods=['POST'])
def upload():
    try:
        file = request.files['file']
        if file:
            file.save(os.path.join(
                app.config['UPLOAD_DIRECTORY'],
                secure_filename(file.filename)
            ))
    except RequestEntityTooLarge:
        return "The File you uploaded is larger than the limit of 16MB."
    return redirect("/modules/post_module")


