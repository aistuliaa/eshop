from sqlalchemy.orm import sessionmaker
from mod.model.idp_classes import Cart, Product, User
from product_crud import engine

Session = sessionmaker(bind=engine)
session = Session()

def get_cart_items(user_id: int):
    """Get all items in a user's cart."""
    try:
        cart_items = (
            session.query(Cart, Product)
            .join(Product, Cart.product_id == Product.id)
            .filter(Cart.user_id == user_id)
            .all()
        )
        return cart_items
    except Exception as e:
        print(f"Error retrieving cart items: {e}")
        return []

def delete_from_cart(user_id: int, product_id: int):
    """Remove a product from the cart."""
    try:
        cart_item = session.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()
        
        if cart_item:
            session.delete(cart_item)
            session.commit()
            print(f"Product {product_id} removed from cart.")
        else:
            print(f"Product {product_id} not found in cart.")
    except Exception as e:
        session.rollback()
        print(f"Error deleting product from cart: {e}")

def add_to_cart(user_id: int, product_id: int, quantity: int):
    """Add a product to the cart."""
    try:
        existing_item = session.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()

        if existing_item:
            existing_item.quantity += quantity
            session.commit()
            print(f"Product quantity updated in cart.")
        else:
            new_cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
            session.add(new_cart_item)
            session.commit()
            print(f"Product added to cart.")
    except Exception as e:
        session.rollback()
        print(f"Error adding product to cart: {e}")
