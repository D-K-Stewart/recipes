from flask import render_template,redirect,request,session,flash
from flask_app import app, bcrypt
from flask_app.models.user import User
from flask_app.models.recipe import Recipe




@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')

    return render_template('index.html')

@app.route('/dashboard')
def get_one():

    if 'user_id' not in session:
        return redirect('/')

    context = {
        'user': User.get_one({'id': session['user_id']}),
        'all_recipes' : Recipe.get_all()
    }
    print(context)
    return render_template('dashboard.html', **context)



@app.route('/create', methods=['POST'])
def create():
    # validate the form here ...
    # create the hash
    print (request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    password = bcrypt.generate_password_hash(request.form['password'])
    print(password)

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email" : request.form["email"],
        "password" : password
    }
    # Call the save @classmethod on User
    User.save(data)
    # store user id into session

    return redirect("/")


@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash(u"Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash(u"Invalid Email/Password", "login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")


@app.route('/logout')
def user():
    session.clear()
    return redirect('/')


# @app.route('/edit/<int:id>')
# def edit_user(id):
#     user = User.data({'id': id})
    
#     return render_template('edit.html', user=user)

# @app.route('/update/<int:id>', methods=["POST"])
# def update_user(id):
#     data = {
#         'id': id,
#         **request.form
#     }
#     User.update(data)
#     return redirect(f'/users/{id}')

@app.route('/users/<int:id>')
def one_user(id):
    user = User.data({'id': id})
    print (user)
    return render_template('read(one).html', user=user)

# @app.route('/show/<int:id>')
# def show_user(id):
#     user = User.data({'id': id})
#     print(user) 
#     return redirect(f'/users/{id}')

# @app.route('/delete/<int:id>', methods=["POST"])
# def delete_user(id):

#     if 'user_id' not in session:
#         return redirect('/')

#     User.delete({'id': id})
#     return redirect('/users')

#----------------------------------------------------------------temps

# @app.route('/dashboard')
# def dashboard_temp():
#     return render_template("dashboard.html")

# @app.route('/show')
# def dashboard_temp():
#     return render_template("show.html")

# @app.route('/edit')
# def dashboard_temp():
#     return render_template("edit.html")

# @app.route('/new')
# def dashboard_temp():
#     return render_template("new.html")



