from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from mod.db.populate_db import engine
from mod.model.idp_classes import Product
from sqlalchemy.exc import SQLAlchemyError

Session = sessionmaker(bind=engine)
session = Session()

def add_product(name, description, price, stock, category=None, rating=0.0):
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
    try:
        products = session.query(Product).all()
        return products
    except SQLAlchemyError as e:
        print(f"Error fetching products: {e}")
        return []

def get_product_by_id(product_id):
    try:
        product = session.query(Product).filter_by(id=product_id).first()
        return product
    except SQLAlchemyError as e:
        print(f"Error fetching product: {e}")
        return None

def update_product(product_id, name=None, description=None, price=None, stock=None, category=None, rating=None):
    try:
        product = session.query(Product).filter_by(id=product_id).first()
        if product:
            if name: product.name = name
            if description: product.description = description
            if price is not None: product.price = price
            if stock is not None: product.stock = stock
            if category: product.category = category
            if rating is not None: product.rating = rating
            session.commit()
            print(f"Product ID {product_id} updated successfully.")
        else:
            print(f"Product ID {product_id} not found.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating product: {e}")

def delete_product(product_id):
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


if __name__ == "__main__":

    add_product(name="Sample Product", description="This is a test product.", price=10.99, stock=50, category="Test")

    products = get_all_products()
    for product in products:
        print(product.name, product.price)

    update_product(product_id=1, price=12.99, stock=45)

    delete_product(product_id=1)
