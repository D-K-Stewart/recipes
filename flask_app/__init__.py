from flask import Flask
app = Flask(__name__)

app.secret_key = 'import os; print(os.urandom(.007!))'


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)