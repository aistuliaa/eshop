from flask import Flask, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from mod.model.idp_classes import User, engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = 'dreamteam'

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                flash("Vartotojo vardas jau užimtas", "error")
                return redirect(url_for('register'))

            hashed_password = generate_password_hash(password, method='sha256')

            new_user = User(username=username, password=hashed_password)

            session.add(new_user)
            session.commit()

            flash("Registracija sėkminga! Galite prisijungti.", "success")
            return redirect(url_for('login_page'))

        except Exception as e:
            session.rollback()  
            flash(f"Įvyko klaida: {str(e)}", "error")
            return redirect(url_for('register'))

    return '''
        <form method="POST">
            Vartotojo vardas: <input type="text" name="username"><br>
            Slaptažodis: <input type="password" name="password"><br>
            <input type="submit" value="Registruotis">
        </form>
        <p><a href="{{ url_for('login_page') }}">Jau turite paskyrą? Prisijunkite</a></p>
    '''

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
