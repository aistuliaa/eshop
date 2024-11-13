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