# balanso perziurejimas ir papildymas

from flask import Flask, request, redirect, url_for, flash, session as flask_session, render_template
from mod.model.idp_classes import User, engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.secret_key = 'dreamteam'  # kaip suprantu reikia sito, kad flash funkcija veiktu

Session = sessionmaker(bind=engine)
session_db = Session()

@app.route('/balance', methods=['GET', 'POST'])
def balance_view():
    user_id = flask_session.get('user_id') 
    
    if user_id:
        user = session_db.query(User).filter_by(id=user_id).first()

        if request.method == 'POST': 
            amount = request.form.get('amount')
            
            try:
                amount = float(amount)
                if amount <= 0:
                    flash('Papildyti balansą galima tik teigiama suma')
                else:
                    user.balance += amount 
                    session_db.commit()  
                    flash(f'Jūsų balansas buvo papildytas {amount} EUR')
            except ValueError:
                flash('Netinkamai įvedėte sumą, patikrinkite ar gerai įvėdėte skaičius')

        return render_template('balansas.html', balance=user.balance)

    else:
        flash('Prašome prisijungti, kad galėtumėte peržiūrėti ir papildyti savo balansą.')
        return redirect(url_for('login_page'))  

if __name__ == '__main__':
    app.run(debug=True)

# jau prisijungus kadangi tik matome, tada galime pasiziureti savo balansa ir jei norime ji papildyti, dar pagaudome klaida, pvz, jei zmogus nori ivest ne 200, o 'du simtai', kad neleistu taip.