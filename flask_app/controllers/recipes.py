from flask import render_template,redirect,request,session,flash
from flask_app import app, bcrypt
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


# @app.route('/')
# @app.route('/recipes')
# def all_recipes():
#     recipes = Recipes.get_all()
#     print(recipes)
#     return render_template('index.html', all_recipes = recipes)


@app.route('/new')
def new_recipe():

    context = {
        'user' : User.get_one({'id':session['user_id']})
    }

    return render_template('new.html', **context)



@app.route('/recipe/<int:id>/show')
def show_recipes(id):
    context = {
        'user': User.get_one({'id': session['user_id']}),
        'recipe': Recipe.get_one({'id': id})

    }
    return render_template("recipes.html", **context)




@app.route('/create_recipe', methods=['POST'])
def create_recipe():


    is_valid = Recipe.validate_recipe(request.form)

    if not is_valid:
        return redirect('/new')

    data = {
        **request.form,
        'user_id' : session['user_id']
        # "name": request.form["name"],
        # "description": request.form["description"],
        # "instructions" : request.form["instructions"],
        # "date_made_on" : request.form["date_made_on"],
    }
    # Call the save @classmethod on User
    Recipe.create(data)
    # store user id into session

    return redirect("/dashboard")



@app.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    recipe = Recipe.get_one({'id': id})

    if recipe.user_id != session['user_id']:
        return redirect('/')

    Recipe.delete_recipe({'id': id})
    return redirect('/')


@app.route('/edit/<int:id>')
def edit_recipe(id):

    recipe = Recipe.get_one({'id': id})

    if recipe.user_id != session['user_id']:
        return redirect('/')

    context = {
        'user': User.get_one({'id': session['user_id']}),
        'recipe' : Recipe.get_one({'id': id})
    }
    return render_template('edit.html', **context)



@app.route('/recipe/<int:id>/update', methods=["POST"])
def update_recipe(id):

    recipe = Recipe.get_one({'id': id})

    if recipe.user_id != session['user_id']:
        return redirect('/')

    is_valid = Recipe.validate_recipe(request.form)

    if not is_valid:
        return redirect(f'recipe/{id}/edit')

    data = {
        **request.form,
        'id':id,
        # 'recipe' : recipe
    }
    recipe = Recipe.update(data)
    return redirect('/dashboard')




