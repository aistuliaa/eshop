from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from mod.model.idp_classes import User, engine
from sqlalchemy.orm import sessionmaker

registracija_blueprint = Blueprint('registracija', __name__, template_folder='templates')

Session = sessionmaker(bind=engine)
session = Session()

@registracija_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            if not username or not email or not password:
                flash("Visi laukai yra privalomi.", "error")
                return redirect(url_for('registracija.register'))

            existing_user = session.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            if existing_user:
                flash("Vartotojo vardas arba el. pašto adresas jau užimtas.", "error")
                return redirect(url_for('registracija.register'))

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            new_user = User(username=username, email=email, password=hashed_password)
            session.add(new_user)
            session.commit()

            flash("Registracija sėkminga! Galite prisijungti.", "success")
            return redirect(url_for('registracija.login_page'))

        except Exception as e:
            session.rollback()
            flash(f"Įvyko klaida registruojant: {str(e)}", "error")
            return redirect(url_for('registracija.register'))

    return render_template('reg.html')

@registracija_blueprint.route('/login')
def login_page():
    return render_template('login.html')

@registracija_blueprint.route('/home')
def home():
    return "Pagrindinis puslapis po prisijungimo."