from flask import render_template, redirect, url_for
from flask import Flask
from model.user_controller import user_blueprint
from flask_login import current_user, login_required

app = Flask(__name__)
app.register_blueprint(user_blueprint)

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('profile'))
    return render_template('admin/dashboard.html')