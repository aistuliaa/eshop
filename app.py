from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, current_user, login_required
from mod.model.user_controller import user_blueprint
from mod.model.registracija import registracija_blueprint
from mod.db import session
from mod.model.idp_classes import Product

app = Flask(__name__, template_folder='mod/templates')
app.secret_key = 'dreamteam'

app.register_blueprint(registracija_blueprint, url_prefix='/')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from mod.model.idp_classes import User
    return User.get(user_id)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cargo')
def get_all_products():
    from mod.model.idp_classes import Product
    from mod.db import session
    products = session.query(Product).all()
    return render_template('prekes.html', products=products)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/reg')
def reg():
    return render_template('reg.html')

@app.route('/pirkejas')
def pirkejas():
    return render_template('pirkejas.html')

@app.route('/loginout')
def loginout():
    return render_template('loginout.html')

@app.route('/balansas')
def balansas():
    return render_template('balansas.html')

@app.route('/add_balansas')
def add_balansas():
    return render_template('add_balansas.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('profile'))
    return render_template('admin/dashboard.html')

# admin meniu

@app.route('/new_cargo')
def new_cargo():
    return render_template('new_cargo.html')

@app.route('/add_cargo')
def add_cargo():
    return render_template('add_cargo.html')

@app.route('/delete_cargo')
def delete_cargo():
    return render_template('delete_cargo.html')

@app.route('/delete_user')
def delete_user():
    return render_template('delete_user.html')

@app.route('/stat_cargo')
def stat_cargo():
    return render_template('stat_cargo.html')



# Run the application
if __name__ == '__main__':
    app.run(debug=True)