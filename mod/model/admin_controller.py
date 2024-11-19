from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from flask_login import login_required, current_user
from mod.model.idp_classes import User, engine, session as db_session, Product
from sqlalchemy.orm import sessionmaker

admin_blueprint = Blueprint("admin", __name__, template_folder="../templates/admin")

Session = sessionmaker(bind=engine)

@admin_blueprint.route("/dashboard")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Prieiga atmesta! Tik administratoriai gali prisijungti prie šio puslapio.", "error")
        return redirect(url_for("home"))
    return render_template("admin_dashboard.html")

@admin_blueprint.route("/add-product", methods=["GET", "POST"])
@login_required
def add_product():
    if not current_user.is_admin:
        flash("Prieiga atmesta! Tik administratoriai gali pasiekti šią funkciją.", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        product_name = request.form.get("name")
        price = request.form.get("price")
        stock = request.form.get("stock")

        if not product_name or not price or not stock:
            flash("Prašome užpildyti visus laukus!", "error")
            return render_template("admin_add_product.html")

        try:
            new_product = Product(name=product_name, price=float(price), stock=int(stock))
            db_session.add(new_product)
            db_session.commit()
            flash(f"Produktas '{product_name}' sėkmingai pridėtas už {price}!", "success")
            return redirect(url_for("admin.admin_dashboard"))
        except Exception as e:
            db_session.rollback()
            flash(f"Klaida pridedant produktą: {e}", "error")
            return render_template("admin_add_product.html")

    return render_template("admin_add_product.html")

@admin_blueprint.route('/update-stock', methods=['GET', 'POST'])
@login_required
def update_stock():
    if not current_user.is_admin:
        flash('Neturite prieigos teisių.', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        new_stock = request.form.get('new_stock')
        try:
            product = db_session.query(Product).get(product_id)
            if product:
                product.stock = int(new_stock)
                db_session.commit()
                flash(f'Prekės "{product.name}" kiekis atnaujintas.', 'success')
            else:
                flash('Prekė nerasta.', 'error')
        except Exception as e:
            db_session.rollback()
            flash(f"Klaida atnaujinant prekių kiekį: {e}", "error")

    products = db_session.query(Product).all()
    return render_template('update_stock.html', products=products)

@admin_blueprint.route('/remove-product', methods=['GET', 'POST'])
@login_required
def remove_product():
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        product = db.session.query(Product).filter_by(id=product_id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            flash(f"Product {product.name} removed successfully!", "success")
        else:
            flash("Product not found.", "error")
        return redirect(url_for('admin.admin_dashboard'))
    
    products = db.session.query(Product).all()
    return render_template('admin_remove_product.html', products=products)

@admin_blueprint.route('/delete-user', methods=['GET', 'POST'])
@login_required
def delete_user():
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for('home'))

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user = db.session.query(User).filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash(f"User {user.username} deleted successfully!", "success")
        else:
            flash("User not found.", "error")
        return redirect(url_for('admin.admin_dashboard'))

    users = db.session.query(User).all()
    return render_template('admin_delete_user.html', users=users)

@admin_blueprint.route('/product-stats', methods=['GET'])
@login_required
def product_stats():
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for('home'))

    products = db.session.query(Product).all()
    stats = [{"name": product.name, "stock": product.stock, "price": product.price} for product in products]

    return render_template('admin_product_stats.html', stats=stats)