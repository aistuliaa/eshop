from flask import Blueprint, render_template
from model.idp_classes import User, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/admin/users')
def view_users():
    users = session.query(User).all()
    return render_template('admin/view_users.html', users=users)