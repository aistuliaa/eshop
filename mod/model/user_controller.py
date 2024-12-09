from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

# Blueprints
user_blueprint = Blueprint('user', __name__, template_folder='templates')
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

# Admin Dashboard
@admin_blueprint.route('/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for('user.user_profile'))
    return render_template('admin.html')

# User Profile
@user_blueprint.route('/user-profile')
@login_required
def user_profile():
    return render_template('user_profile.html')

# Admin: View Users
@admin_blueprint.route('/users')
@login_required
def view_users():
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for('user.user_profile'))
    # Add logic to fetch and display users
    return render_template('view_users.html')

# Admin: Manage Products
@admin_blueprint.route('/products')
@login_required
def manage_products():
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for('user.user_profile'))
    # Add logic to fetch and display products
    return render_template('manage_products.html')

# Admin: Add Product
@admin_blueprint.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for('user.user_profile'))
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        if not product_name:
            flash("Product name is required.", "error")
            return redirect(url_for('admin.add_product'))
        # Add product save logic here
        flash(f"Product '{product_name}' added successfully!", "success")
        return redirect(url_for('admin.manage_products'))
    return render_template('add_product.html')

# Admin: View Orders
@admin_blueprint.route('/orders')
@login_required
def view_orders():
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for('user.user_profile'))
    # Add logic to fetch and display orders
    return render_template('view_orders.html')