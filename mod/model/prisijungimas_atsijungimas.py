from flask import Flask, render_template, request, redirect, url_for, flash, session as flask_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from mod.model.idp_classes import User, engine

app = Flask(__name__)
app.secret_key = 'dreamteam'

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
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
                flask_session['is_admin'] = user.is_admin
                flash('Prisijungimas sėkmingas', 'success')

                if user.is_admin:
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('home'))
            else:
                user.failed_logins += 1
                if user.failed_logins >= 3:
                    user.is_blocked = True
                session.commit()
                remaining_attempts = 3 - user.failed_logins
                flash(f"Neteisingas slaptažodis. Likę bandymai: {remaining_attempts}", 'error')
                return redirect(url_for('login'))

        return render_template('login.html')

    except SQLAlchemyError as e:
        flash(f"Database error: {e}", 'error')
        return redirect(url_for('login'))
    except Exception as e:
        flash(f"Unexpected error: {e}", 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    try:
        flask_session.pop('user_id', None)
        flask_session.pop('username', None)
        flask_session.pop('is_admin', None)
        flash('Sėkmingai atsijungėte.', 'success')
    except Exception as e:
        flash(f"Unexpected error during logout: {e}", 'error')

    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user_id' in flask_session:
        username = flask_session.get('username')
        return render_template('index.html', username=username, is_admin=flask_session.get('is_admin', False))
    return render_template('index.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if flask_session.get('is_admin'):
        return render_template('admin_dashboard.html')
    else:
        flash('Jūs neturite prieigos prie šio puslapio.', 'error')
        return redirect(url_for('home'))

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Failed to start the application: {e}")
