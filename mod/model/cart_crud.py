from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from mod.model.idp_classes import Cart, User, Product, Review
from mod.db.populate_db import engine

Session = sessionmaker(bind=engine)
session = Session()


def add_to_cart(user_id: int, product_id: int, quantity: int):
    try:
        existing_item = session.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()

        if existing_item:
            existing_item.quantity += quantity
            print("Product quantity updated in the cart.")
        else:
            new_cart = Cart(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
            session.add(new_cart)
            print("Product added to cart successfully.")
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding product to cart: {e}")


def delete_from_cart(user_id: int, product_id: int):
    try:
        cart_item = session.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()

        if cart_item:
            session.delete(cart_item)
            session.commit()
            print(f"Product ID {product_id} removed from the cart.")
        else:
            print(f"Product ID {product_id} not found in the cart.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error removing product from cart: {e}")


def get_cart_items(user_id: int):
    try:
        cart_items = (
            session.query(Cart, Product)
            .join(Product, Cart.product_id == Product.id)
            .filter(Cart.user_id == user_id)
            .all()
        )
        return cart_items
    except SQLAlchemyError as e:
        print(f"Error retrieving cart items: {e}")
        return []


def checkout_cart(user_id: int):
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print("User not found.")
            return

        cart_items = get_cart_items(user_id)

        if not cart_items:
            print("Cart is empty.")
            return

        total_price = sum(cart_item.quantity * product.price for cart_item, product in cart_items)

        if user.balance < total_price:
            print("Insufficient balance. Please add funds to your account.")
            return

        user.balance -= total_price

        for cart_item, product in cart_items:
            if product.stock < cart_item.quantity:
                print(f"Insufficient stock for {product.name}.")
                return
            product.stock -= cart_item.quantity
            session.delete(cart_item)

        session.commit()
        print("Checkout successful!")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error during checkout: {e}")


# Example integration functions for Flask views

def handle_add_to_cart(user_id, product_id, quantity):
    add_to_cart(user_id, product_id, quantity)
    return "Product added to cart."


def handle_view_cart(user_id):
    cart_items = get_cart_items(user_id)
    return [
        {
            "product_name": product.name,
            "quantity": cart_item.quantity,
            "total_price": cart_item.quantity * product.price
        }
        for cart_item, product in cart_items
    ]


def handle_checkout(user_id):
    checkout_cart(user_id)
    return "Checkout completed successfully."
