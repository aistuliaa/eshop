# 1.Prisijungimas (neteisingai mėginant prisijungti 3 ar daugiau kartų turėtų būti užblokuotas prisijungimas)
# pip install flask flask-login sqlalchemy
# padariau ir kad atsijungimas butu, o po to mestu i pagr puslapi

# padariau, kad hashuoti slaptazodziai

from flask import Flask, render_template, request, redirect, url_for, flash, session as flask_session
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from mod.model.idp_classes import User, engine

app = Flask(__name__)
app.secret_key = 'dreamteam'
# nesu tikra ar mums butent sito reikia

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

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
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user_id' in flask_session:
        username = flask_session['username']
        return render_template('index.html', username=username)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)