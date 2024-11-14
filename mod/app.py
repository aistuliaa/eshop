from flask import Flask, render_template

# Inicializuojame Flask aplikaciją
app = Flask(__name__)

# Sukuriame pagrindinį maršrutą, kuris grąžins pagrindinį puslapį
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cargo')
def prekes():
    prekes = ["NOTV", "MTV", "TV"]
    return render_template('prekes.html', prekes=prekes)

@app.route('/login')
def login():    
    return render_template('login.html')

@app.route('/reg')
def reg():    
    return render_template('reg.html')

@app.route('/pirkejas')
def pirkejas():
    
    return render_template('pirkejas.html')

@app.route('/loginout')
def loginout():    
    return render_template('loginout.html')

@app.route('/balansas')
def balansas():    
    return render_template('balansas.html')

@app.route('/add_balansas')
def add_balansas():    
    return render_template('add_balansas.html')
# Aplikacijos paleidimas
if __name__ == '__main__':
    app.run(debug=True)