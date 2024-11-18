from flask import Flask, request, render_template, url_for, redirect, flash, session as flask_session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from mod.model.user_controller import user_blueprint
from mod.model.registracija import registracija_blueprint
from mod.db import session
from mod.model.idp_classes import User, Product

app = Flask(__name__, template_folder='mod/templates')
app.secret_key = 'dreamteam'

app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(registracija_blueprint, url_prefix='/auth')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')

from flask import request, render_template
from sqlalchemy import and_

@app.route('/cargo')
def get_all_products():
    # Gauti užklausos parametrus
    sort_by = request.args.get('sort', 'name')  # Numatytoji rūšiavimo reikšmė
    category = request.args.get('category', '')  # Filtras pagal kategoriją
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    search = request.args.get('search', '')  # Paieška pagal pavadinimą

    # Užklausa į duomenų bazę
    query = session.query(Product)

    # Filtravimas pagal kategoriją
    if category:
        query = query.filter(Product.category == category)

    # Filtravimas pagal kainos intervalą
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # Filtravimas pagal pavadinimą (paieška)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    # Rūšiavimas
    if sort_by in ['name', 'price', 'rating', 'category']:
        query = query.order_by(getattr(Product, sort_by))
    
    # Gauti rezultatus
    products = query.all()

    return render_template('prekes.html', products=products)


# @app.route('/cargo')
# def get_all_products():
#     from mod.model.idp_classes import Product
#     from mod.db import session
#     products = session.query(Product).all()
#     return render_template('prekes.html', products=products)

# @app.route('/cargo')
# def get_all_products():
#     """Display all products."""
#     products = session.query(Product).all()
#     return render_template('prekes.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login functionality."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = session.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flask_session['user_id'] = user.id
            flask_session['username'] = user.username
            flash('Prisijungta sėkmingai!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Neteisingas vartotojo vardas arba slaptažodis.', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Handle logout functionality."""
    logout_user()
    flask_session.clear()
    flash('Sėkmingai atsijungėte.', 'success')
    return redirect(url_for('home'))

# @app.route('/pirkejas')
# @login_required
# def pirkejas():
#     """Render the customer page."""
#     if 'user_id' in flask_session:
#         user = session.query(User).get(flask_session['user_id'])
#         if user:
#             return render_template('pirkejas.html', user=user)
#     flash('Norint pasiekti šį puslapį, reikia prisijungti.', 'error')
#     return redirect(url_for('login'))

@app.route('/balansas')
@login_required
def balansas():
    """Display user balance."""
    if 'user_id' in flask_session:
        user = session.query(User).get(flask_session['user_id'])
        if user:
            return render_template('balansas.html', balance=user.balance)
    flash('Norint pasiekti šį puslapį, reikia prisijungti.', 'error')
    return redirect(url_for('login'))

@app.route('/add_balansas')
@login_required
def add_balansas():
    """Render page for adding balance."""
    return render_template('add_balansas.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    """Render the admin dashboard."""
    if current_user.role != 'admin':
        flash('Neturite prieigos teisių.', 'error')
        return redirect(url_for('home'))
    return render_template('admin/dashboard.html')

@app.route('/pirkejas')
@login_required
def pirkejas():
    """Render the customer page."""
    if 'user_id' in flask_session:
        user = session.query(User).get(flask_session['user_id'])
        if user:
            return render_template('pirkejas.html', user=user)
    flash('Norint pasiekti šį puslapį, reikia prisijungti.', 'error')
    return redirect(url_for('login'))


# Run the application
if __name__ == '__main__':
    app.run(debug=True)