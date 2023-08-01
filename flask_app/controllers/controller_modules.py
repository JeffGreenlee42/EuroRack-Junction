from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash, jsonify
from flask_app.models.model_module import Module
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge, BadRequest
# from flask import Flaskform
# from flask import FileField 
import os
import uuid


@app.route("/marketplace")
def modules():
    if 'user_id' not in session:
        session.clear()
        return render_template("/")
    all_modules = []
    # print("About to enter Module.get_all()")
    modules = Module.get_all()
    # print(f"In controller modules() modules is {modules}")
    for module in modules:
        a_module = {
            'module_id': module['modules.id'],
            'module_name': module['module_name'],
            'maker': module['maker'],
            'function': module['function'],
            'panel_finish': module['panel_finish'],
            'hp': module['hp'],
            'one_u': module['one_u'],
            'condition': module['condition'],
            'photo': module['photo'],
            'users_id': module['users_id'],
            'price': module['price'],
            'description': module['description']
        }
        all_modules.append(a_module)
        # print(f"all_modules is {all_modules}")
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
        'users_id': session['user_id'],
        'price': 0,
        'shipping': 0,
        'description': ''
    }
    return render_template("new_module.html", module = module)

@app.route("/modules/add_module", methods=["POST"])
def add_module():
    if 'user_id' not in session:
        return redirect("/logout")
    if 'photo_file_name' not in session:
        session['photo_file_name'] = 'NO_PHOTO'
    one_u_value = request.form.get('one_u', type=int)
    if one_u_value == 1:
        one_u_value = 1
    else:
        one_u_value = 0
    module = {
            # 'module_id': request.form['module_id'],
            'module_name': request.form['module_name'],
            'maker': request.form['maker'],
            'function': request.form['function'],
            'panel_finish': request.form['panel_finish'],
            'hp': request.form['hp'],
            'one_u': one_u_value,
            'condition': request.form['condition'],
            'photo': session['photo_file_name'],
            'users_id': request.form['users_id'],
            'price': request.form['price'],
            'shipping': request.form['shipping'],
            'description': request.form['description']
    }
    valid = Module.validate_module(request.form)
    if valid:
        # print(f"add_module() request.form is: {request.form}")
        Module.add_module(module)
        return redirect("/marketplace")
    return render_template("new_module.html", module = module)

@app.route("/modules/get_one/<int:module_id>")
def get_one(module_id):
    # print(f"module_id is {module_id}")
    module = Module.get_one(module_id)
    # print(f"in controller - get_One() module is {module}")
    if not module:
        return redirect("/marketplace")
    return render_template("display_module.html", module = module)

@app.route("/modules/edit_module/<int:module_id>")
def edit_module(module_id):
    if 'user_id' not in session:
        redirect("/")
    module = Module.get_one(module_id)
    if not module:
        return redirect("/modules")
    return render_template("edit_module.html", module = module)

@app.route("/modules/update_module", methods=['POST'])
def change_module():
    print(f"change_module: request.form: {request.form}")
    one_u = request.form.get('one_u', type=int, default=0)
    module_id = request.form.get("module_id")
    valid = Module.validate_module(request.form)
    if not valid:
        return render_template("edit_module.html", module = request.form )
    data = {
        "module_id": module_id,
        "module_name": request.form['module_name'],
        "maker": request.form['maker'],
        "function": request.form['function'],
        "panel_finish": request.form['panel_finish'],
        "hp": int(request.form['hp']),
        "one_u": one_u,
        "condition": request.form['condition'],
        "photo": session['photo_file_name'],
        "price": int(request.form['price']),
        "shipping": int(request.form['shipping']),
        "description": request.form['description']
    }
    print(f"Controller - change module: data is {data}")
    result = Module.change_module(data)
    print(f"Controller - change_module: result is {result}")
    return redirect("/marketplace")

@app.route("/modules/delete/<int:module_id>")
def delete_module(module_id):
    module_id = {
        'module_id': module_id
    }
    Module.delete_module(module_id)
    return redirect("/marketplace")

@app.route("/upload", methods=['POST'])
def upload():
    try:
        file = request.files.get('file')  # Use get() to handle missing 'file' key gracefully
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_DIRECTORY'], filename))

            session['photo_file_name'] = filename
            photo_url = f"{request.url_root}images/uploads/{filename}"
            print(f"Uploaded photo URL: {photo_url}") 
            return jsonify({"photo_url": photo_url})
        else:
            # Handle case when 'file' key is missing in the request
            raise BadRequest("No file uploaded.")
    except RequestEntityTooLarge:
        return "The File you uploaded is larger than the limit of 16MB."
    except Exception as e:
        # Handle any other unexpected error during file upload or saving
        return f"Error: {str(e)}"

    # If no file was uploaded or there was an error, provide a response
    print(f"In controller: upload() session['photo_file_name'] is {session['photo_file_name']}")
    return redirect("/modules/post_module")


# def upload():
#     try:
#         file = request.files['file']
#         if file:
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_DIRECTORY'],filename))
#             session['photo_file_name'] = filename
#             photo_url = f"{request.url_root}static/images/uploads/{filename}"
#             print(f"Uploaded photo URL: {photo_url}") 
#             return jsonify({"photo_url": photo_url})
#     except RequestEntityTooLarge:
#         return "The File you uploaded is larger than the limit of 16MB."
#     print(f"in controller: upload() session['photo_file_name] is {session['photo_file_name']}")
#     return redirect("/modules/post_module")


