from flask import Flask, request, redirect, url_for, flash, session, render_template
from mod.model.idp_classes import User, engine
from sqlalchemy.orm import sessionmaker
from flask_login import login_required

app = Flask(__name__)
app.secret_key = 'dreamteam'  # Pasirūpinkite, kad turėtumėte šį raktą flash žinutėms

Session = sessionmaker(bind=engine)
session_db = Session()

@app.route('/balansas')
@login_required
def balansas():
    """Display user balance."""
    if 'user_id' in session:
        user = session_db.query(User).get(session['user_id'])
        if user:
            print(f"Vartotojo balansas rodomas: {user.balance}")  # Patikriname, ar balansas rodomas teisingai
            return render_template('balansas.html', balance=user.balance)
    flash('Norint pasiekti šį puslapį, reikia prisijungti.', 'error')
    return redirect(url_for('login_page'))  # Peradresuojame į prisijungimą, jei vartotojas nėra prisijungęs

@app.route('/add_balansas', methods=['GET', 'POST'])
@login_required
def add_balansas():
    """Add funds to user balance."""
    user_id = session.get('user_id')  # Tikriname, ar vartotojas prisijungęs

    if user_id:
        if request.method == 'POST':  # Jei tai POST užklausa
            amount = request.form.get('amount')  # Paima įvestą sumą
            try:
                amount = float(amount)
                if amount <= 0:
                    flash('Papildyti balansą galima tik teigiama suma')
                else:
                    # Patikriname, ar vartotojas tikrai rastas
                    user = session_db.query(User).filter_by(id=user_id).first()
                    if user:
                        print(f"Pradinis balansas: {user.balance}")
                        user.balance += amount  # Atnaujiname balansą
                        session_db.flush()  # Siunčiame užklausą į DB
                        session_db.commit()  # Patvirtiname pakeitimus
                        print(f"Balansas po papildymo: {user.balance}")  # Patikriname, ar balansas buvo atnaujintas
                        flash(f'Jūsų balansas buvo papildytas {amount:.2f} EUR', 'success')
                        return redirect(url_for('balansas'))  # Peradresuojame į balanso puslapį
                    else:
                        flash('Vartotojas nerastas.', 'error')
            except ValueError:
                flash('Netinkamai įvedėte sumą, patikrinkite ar gerai įvėdėte skaičius.', 'error')
                return redirect(url_for('add_balansas'))

        return render_template('add_balansas.html')

    else:
        flash('Prašome prisijungti, kad galėtumėte papildyti savo balansą.', 'error')
        return redirect(url_for('login_page'))  # Jei vartotojas nėra prisijungęs, nukreipiame į login puslapį


if __name__ == '__main__':
    app.run(debug=True)




# jau prisijungus kadangi tik matome, tada galime pasiziureti savo balansa ir jei norime ji papildyti, dar pagaudome klaida, pvz, jei zmogus nori ivest ne 200, o 'du simtai', kad neleistu taip.