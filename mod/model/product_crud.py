from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from mod.db.populate_db import engine
from mod.model.idp_classes import Product
from sqlalchemy.exc import SQLAlchemyError

Session = sessionmaker(bind=engine)
session = Session()

def add_product(name, description, price, stock, category=None, rating=0.0):
    """Add a new product to the database."""
    try:
        new_product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            rating=rating
        )
        session.add(new_product)
        session.commit()
        print(f"Product '{name}' added successfully.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding product: {e}")

def get_all_products():
    """Retrieve all products from the database."""
    try:
        products = session.query(Product).all()
        return products
    except SQLAlchemyError as e:
        print(f"Error fetching products: {e}")
        return []

def get_product_by_id(product_id):
    """Retrieve a product by its ID."""
    try:
        product = session.query(Product).filter_by(id=product_id).first()
        return product
    except SQLAlchemyError as e:
        print(f"Error fetching product: {e}")
        return None

def update_product(product_id, name=None, description=None, price=None, stock=None, category=None, rating=None):
    """Update the details of an existing product."""
    try:
        product = session.query(Product).filter_by(id=product_id).first()
        if product:
            if name is not None:
                product.name = name
            if description is not None:
                product.description = description
            if price is not None:
                product.price = price
            if stock is not None:
                product.stock = stock
            if category is not None:
                product.category = category
            if rating is not None:
                product.rating = rating
            session.commit()
            print(f"Product ID {product_id} updated successfully.")
        else:
            print(f"Product ID {product_id} not found.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating product: {e}")

def delete_product(product_id):
    """Delete a product by its ID."""
    try:
        product = session.query(Product).filter_by(id=product_id).first()
        if product:
            session.delete(product)
            session.commit()
            print(f"Product ID {product_id} deleted successfully.")
        else:
            print(f"Product ID {product_id} not found.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error deleting product: {e}")

def reduce_stock(product_id, quantity):
    """Reduce the stock of a product after adding to the cart or purchase."""
    try:
        product = get_product_by_id(product_id)
        if product and product.stock >= quantity:
            product.stock -= quantity
            session.commit()
            print(f"Reduced stock for product ID {product_id} by {quantity}. Remaining stock: {product.stock}.")
        else:
            print(f"Not enough stock for product ID {product_id}.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error reducing stock: {e}")
