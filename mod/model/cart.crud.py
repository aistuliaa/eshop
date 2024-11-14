from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from mod.model.idp_classes import Cart
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


# add_to_cart(2, 2, 14)

def delete_from_cart(user_id: int, product_id: int, quantity: int):
    try:
        existing_item = session.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()

        if existing_item:
            amount_delete = int(input(f"How many products do you want to delete: {product_id}"))

            if amount_delete >= existing_item.quantity:
                amount_delete = existing_item.quantity
    except SQLAlchemyError as e:
        print(f"Error deleting product from cart {e}")

    
            
