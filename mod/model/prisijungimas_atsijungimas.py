# 1.Prisijungimas (neteisingai mėginant prisijungti 3 ar daugiau kartų turėtų būti užblokuotas prisijungimas)
# pip install flask flask-login sqlalchemy
# padariau ir kad atsijungimas butu, o po to mestu i pagr puslapi

# padariau, kad hashuoti slaptazodziai

from flask import Flask, render_template, request, redirect, url_for, flash, session as flask_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from mod.model.idp_classes import User, engine

app = Flask(__name__)
<<<<<<< HEAD
app.secret_key = 'dreamteam'  # nesu tikra ar mums butent sito reikia
=======
app.secret_key = 'dreamteam'
# nesu tikra ar mums butent sito reikia
>>>>>>> Funkciju_su_puslapiu_apjungimas

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

<<<<<<< HEAD
            try:
                user = session.query(User).filter_by(username=username).first()
            except SQLAlchemyError as e:
                flash(f"Database error: {e}")  # Klaida susiejant su duomenų baze
                return redirect(url_for('login'))

            if user is None:
                flash('Vartotojas su tokiu prisijungimo vardu nerastas')
                return redirect(url_for('login'))

            if user.is_blocked: # True arba False
                flash('Prisijungimas užblokuotas dėl per daug nesėkmingų bandymų')
                return redirect(url_for('login'))

            if check_password_hash(user.password, password):  # Jei slaptažodis teisingas
                try:
                    user.failed_logins = 0  # Nustatome nesėkmingų bandymų skaičių į 0
                    session.commit()
                except SQLAlchemyError as e:
                    flash(f"Database error: {e}")
                    return redirect(url_for('login'))

                flash('Prisijungimas sėkmingas')
                return redirect(url_for('home'))
            else:
                try:
                    user.failed_logins += 1
                    if user.failed_logins >= 3:
                        user.is_blocked = True  # Blokuojame vartotoją po trijų bandymų
                    session.commit()
                except SQLAlchemyError as e:
                    flash(f"Database error: {e}")
                    return redirect(url_for('login'))

                flash(f"Neteisingas slaptažodis. Likę bandymai: {3 - user.failed_logins}")
                return redirect(url_for('login'))
        else:
            return render_template('login.html')
    except Exception as e:
        flash(f"Unexpected error: {e}")  # Klaida kurios man nepavymo nuspeti
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    try:
        flask_session.pop('user_id', None)  # Išvalome naudotojo sesiją
        flash('Sėkmingai atsijungėte.')  # Pateikiame atsijungimo žinutę
    except KeyError:
        flash('Atsijungimo klaida.')
    except Exception as e:
        flash(f"Unexpected error: {e}")  # Klaida kurios man nepavymo nuspeti
=======
        user = session.query(User).filter_by(username=username).first()
        if not user:
            flash('Vartotojas su tokiu prisijungimo vardu nerastas', 'error')
            return redirect(url_for('login'))
        
        if user.is_blocked:
            flash('Prisijungimas užblokuotas dėl per daug nesėkmingų bandymų', 'error')
            return redirect(url_for('login'))
        
        if check_password_hash(user.password, password):
            user.failed_logins = 0
            session.commit()
            
            flask_session['user_id'] = user.id
            flask_session['username'] = user.username
            flash('Prisijungimas sėkmingas', 'success')
            return redirect(url_for('home'))
    # cia graziname i pagrindini puslapi, kurio vardas nezinau ar bus toks, todel cia ir pasizymiu
        else:
            user.failed_logins += 1  # cia jau padidinam skaiciu nesekmingu
            if user.failed_logins >= 3:
                user.is_blocked = True  # blokas po triju nesegeru
            session.commit()
            remaining_attempts = 3 - user.failed_logins
            flash(f"Neteisingas slaptažodis. Likę bandymai: {remaining_attempts}", 'error')
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    flask_session.pop('user_id', None)
    flask_session.pop('username', None)
    flash('Sėkmingai atsijungėte.', 'success')
>>>>>>> Funkciju_su_puslapiu_apjungimas
    return redirect(url_for('login'))

@app.route('/home')
def home():
<<<<<<< HEAD
    return "Pagrindinis puslapis po prisijungimo."  # Placeholder pagrindiniam puslapiui
=======
    if 'user_id' in flask_session:
        username = flask_session['username']
        return render_template('index.html', username=username)
    return render_template('index.html')
>>>>>>> Funkciju_su_puslapiu_apjungimas

if __name__ == '__main__':
    try:
        app.run(debug=True)  # Paleidžiame Flask programą
    except Exception as e:
        print(f"Failed to start the application: {e}")  # Klaida paleidžiant aplikaciją
