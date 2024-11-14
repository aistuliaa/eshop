# 1.Prisijungimas (neteisingai mėginant prisijungti 3 ar daugiau kartų turėtų būti užblokuotas prisijungimas)
# pip install flask flask-login sqlalchemy

# padariau, kad hashuoti slaptazodziai

from flask import Flask, request, redirect, url_for, flash
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from mod.model.idp_classes import User, engine

app = Flask(__name__)
app.secret_key = 'dreamteam' 
# nesu tikra ar mums butent sito reikia

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = session.query(User).filter_by(username=username).first()
    if user is None:
        flash('Vartotojas su tokiu prisijungimo vardu nerastas')
        return redirect(url_for('login'))
    if user.is_bloked:
        flash('Prisijungimas užblokuotas dėl per daug nesėkmingų bandymų')
    if check_password_hash(user.password, password):
        user.failed_logns = 0
        session.commit()
        flash('Prisijungimas sėkmingas')
        return redirect(url_for('home'))
    # cia graziname i pagrindini puslapi, kurio vardas nezinau ar bus toks, todel cia ir pasizymiu
    else:
        user.failed_logins += 1  # cia jau padidinam skaiciu nesekmingu
        if user.failed_logins >= 3:
            user.is_blocked = True  # blokas po triju nesegeru
        session.commit()
        flash(f"Neteisingas slaptažodis. Likę bandymai: {3 - user.failed_logins}")
        return redirect(url_for('login'))
    
@app.route('/login')
def login_page():
    return '''
        <form method="POST">
            Vartotojo vardas: <input type="text" name="username"><br>
            Slaptažodis: <input type="password" name="password"><br>
            <input type="submit" value="Prisijungti">
        </form>
    '''

@app.route('/home')
def home():
    return "Pagrindinis puslapis po prisijungimo."

if __name__ == '__main__':
    app.run(debug=True)