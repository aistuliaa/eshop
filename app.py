from flask import render_template, redirect, url_for
from flask import Flask
from mod.model.user_controller import user_blueprint
from flask_login import current_user, login_required

app = Flask(__name__)
app.register_blueprint(user_blueprint)

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('profile'))
    return render_template('admin/dashboard.html')
from flask import Flask, render_template

# Inicializuojame Flask aplikaciją
app = Flask(__name__)

# Sukuriame pagrindinį maršrutą, kuris grąžins pagrindinį puslapį
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prekes')
def prekes():
    prekes = ["NOTV", "MTV", "TV"]
    return render_template('prekes.html', prekes=prekes)

@app.route('/admin')
def admin():    
    return render_template('admin.html')

@app.route('/pirkejas')
def pirkejas():
    
    return render_template('pirkejas.html')

# Aplikacijos paleidimas
if __name__ == '__main__':
    app.run(debug=True)