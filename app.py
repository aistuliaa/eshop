from flask import Flask, render_template
from sqlalchemy.orm import sessionmaker
from mod.populate_db import engine, Product  # Importuokite engine ir Product

# Inicializuojame Flask aplikaciją
app = Flask(__name__)

# SQLAlchemy sesijos konfigūracija
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__, template_folder='mod/templates')

app.register_blueprint(user_blueprint)

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('profile'))
    return render_template('admin/dashboard.html')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from mod.model.idp_classes import User
    return User.get(user_id)

# Sukuriame pagrindinį maršrutą, kuris grąžins pagrindinį puslapį
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

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

if __name__ == '__main__':
    app.run(debug=True)