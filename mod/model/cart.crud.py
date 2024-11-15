from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from mod.model.idp_classes import Cart, User, Product, Review
from product_crud import engine

Session = sessionmaker(bind=engine)
session = Session()

def add_to_cart(user_id: int, product_id: int, quantity: int):
    try:
        existing_item = session.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()

        if existing_item:
            existing_item.quantity += quantity
            print(f"You already have this product in the cart. We increase quantity")

        else: 
            new_cart = Cart(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )        
            session.add(new_cart)
            print(f"Product added to cart successfully.")
        session.commit()
        
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding product to cart: {e}")


# add_to_cart(2, 1, 3)

def delete_from_cart(user_id: int, product_id: int, quantity: int):
    try:
        existing_item = session.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()

        if existing_item:

            if quantity >= existing_item.quantity:
                session.delete(existing_item)
                print(f"Product ID {product_id} removed from cart.")
            else:
                existing_item.quantity -= quantity
                print(f"Reduced quantity of product ID {product_id} by {quantity}.")
            session.commit()
        else:
            print(f"Product ID {product_id} not found in user's cart.")

    except SQLAlchemyError as e:
        print(f"Error deleting product from cart {e}")

# delete_from_cart(3, 1, 2)

def get_products_in_cart(user_id): # si funkcija yra nebutina. Jos galima niekur nedeti
    try:
        products = (
            session.query(Product.name)
            .join(Cart, Product.id == Cart.product_id)
            .filter(Cart.user_id == user_id)
            .all()
        )

        product_names = [product.name for product in products]
        print(f"Products in user {user_id}'s cart:", product_names)
        return product_names
    except SQLAlchemyError as e:
        print(f"Error retrieving products from cart: {e}")
        return []

# get_products_in_cart(2)


def checkout_cart_with_review(user_id):
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print("User not found.")
            return
        
        cart_items = (
            session.query(Cart, Product)
            .join(Product, Cart.product_id == Product.id)
            .filter(Cart.user_id == user_id)
            .all()
        )

        if not cart_items:
            print("Cart is empty.")
            return

        total_price = sum(cart_item.quantity * product.price for cart_item, product in cart_items)

        print(f"Products in cart for user {user_id}:")
        for cart_item, product in cart_items:
            print(f"- {product.name}: {cart_item.quantity} x {product.price} = {cart_item.quantity * product.price}")
        print(f"Total price: {total_price}")
        print(f"User: {user_id} Balance: {user.balance}")

        if user.balance < total_price:
            print("Insufficient balance. Please add funds to your account.")
            return

        user.balance -= total_price

        purchased_products = []
        for cart_item, product in cart_items:
            if product.stock < cart_item.quantity:
                print(f"Insufficient stock for {product.name}. Please adjust your cart.")
                return
            product.stock -= cart_item.quantity
            purchased_products.append(product)
            session.delete(cart_item)

        session.commit()
        print(f"Checkout successful! {total_price} has been deducted from your balance.")

        for product in purchased_products:
            print(f"Would you like to leave a review for {product.name}? (yes/no)")
            leave_review = input().strip().lower()
            if leave_review == "yes":
                rating = int(input("Enter a rating (1-5): "))
                comment = input("Enter a comment: ").strip()
                new_review = Review(
                    user_id=user_id,
                    product_id=product.id,
                    rating=rating,
                    comment=comment
                )
                session.add(new_review)

        session.commit()
        print("Thank you for your reviews!")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error during checkout or review submission: {e}")
    finally:
        session.close()

checkout_cart_with_review(2)
