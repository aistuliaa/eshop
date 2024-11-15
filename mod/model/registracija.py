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
            password = request.form.get('password')

            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                flash("Vartotojo vardas jau užimtas", "error")
                return redirect(url_for('registracija.register'))

            hashed_password = generate_password_hash(password, method='sha256')

            new_user = User(username=username, password=hashed_password)

            session.add(new_user)
            session.commit()

            flash("Registracija sėkminga! Galite prisijungti.", "success")
            return redirect(url_for('login_page'))

        except Exception as e:
            session.rollback()
            flash(f"Įvyko klaida: {str(e)}", "error")
            return redirect(url_for('registracija.register'))

    return render_template('reg.html')

@registracija_blueprint.route('/login')
def login_page():
    return render_template('login.html')

@registracija_blueprint.route('/home')
def home():
    return "Pagrindinis puslapis po prisijungimo."