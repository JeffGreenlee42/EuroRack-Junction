from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.model_recipe import Recipe

@app.route("/marketplace")
def recipes():
    if 'user_id' not in session:
        session.clear()
        return render_template("/")
    all_recipes = []
    recipes = Recipe.get_all()
    for recipe in recipes:
        under30 = "No"
        if recipe['under30'] > 0:
            under30 = "Yes"
        a_recipe = {
            'recipe_id': recipe['recipe_id'],
            'name': recipe['name'],
            'under30': under30,
            'posted_by': recipe['first_name']
        }
        all_recipes.append(a_recipe)
    return render_template('recipes.html', all_recipes = all_recipes)



@app.route("/recipes/create_recipe")
def create_recipe():
    recipe = {
        'recipe_name': '',
        'description': '',
        'instructions': '',
        'date_made': '',
        'under30': ''
    }
    return render_template("new_recipe.html", recipe = recipe)

@app.route("/recipes/add_recipe", methods=["POST"])
def add_recipe():
    if 'user_id' not in session:
        return redirect("/logout")
    valid = Recipe.validate_recipe(request.form)
    if valid:
        Recipe.add_recipe(request.form)
        return redirect("/recipes")
    recipe = {
        'recipe_name': request.form['recipe_name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under30': request.form['under30']
    }
    return render_template("new_recipe.html", recipe = recipe)

    return redirect("/recipes")

@app.route("/recipes/get_one/<int:recipe_id>")
def get_one(recipe_id):
    recipe = Recipe.get_one(recipe_id)
    if not recipe:
        return redirect("/recipes")
    return render_template("display_recipe.html", recipe = recipe)

@app.route("/recipes/edit_recipe/<int:recipe_id>")
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        redirect("/")
    recipe = Recipe.get_one(recipe_id)
    if not recipe:
        return redirect("/recipes")
    return render_template("edit_recipe.html", recipe = recipe)
    
@app.route("/recipes/update_recipe", methods=['POST'])
def change_recipe():
    valid = Recipe.validate_recipe(request.form)
    if not valid:
        return render_template("edit_recipe.html", recipe = request.form )
    result = Recipe.change_order(request.form)
    return redirect("/recipes")

@app.route("/recipes/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
    recipe_id = {
        'recipe_id': recipe_id
    }
    Recipe.delete_recipe(recipe_id)
    return redirect("/recipes")


