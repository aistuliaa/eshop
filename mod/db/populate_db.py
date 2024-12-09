import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from mod.model.idp_classes import Base, User, Product, Cart, Order, OrderItem, Review, AuditLog 

engine = create_engine('sqlite:///mod/db/duombaze.db', echo=False)
Base.metadata.create_all(engine)  # Ensures all tables are created
Session = sessionmaker(bind=engine)
session = Session()
# Base.metadata.drop_all(bind=engine) # Istrina visus tables 1/2
# session.commit() # Istrina visus tables 2/2
try:
    user1 = User(username="user1", email="user1@example.com", password="hashed_password1")
    user2 = User(username="user2", email="user2@example.com", password="hashed_password2", balance=100.0)
    admin = User(username="admin", email="admin@example.com", password="hashed_admin", role="admin")

    session.add_all([user1, user2, admin])


    product1 = Product(name="Laptop", description="A high-performance laptop", price=15.0, stock=5, category="Electronics")
    product2 = Product(name="Smartphone", description="A smartphone with a great camera", price=800.0, stock=10, category="Electronics")
    product3 = Product(name="Headphones", description="Noise-cancelling headphones", price=200.0, stock=15, category="Accessories")

    session.add_all([product1, product2, product3])


    order1 = Order(user_id=1, total_amount=2300.0, order_date=datetime.datetime.utcnow(), status="completed")
    order2 = Order(user_id=2, total_amount=800.0, order_date=datetime.datetime.utcnow(), status="pending")

    session.add_all([order1, order2])


    order_item1 = OrderItem(order_id=1, product_id=1, quantity=1, price_at_purchase=1500.0)
    order_item2 = OrderItem(order_id=1, product_id=2, quantity=1, price_at_purchase=800.0)
    order_item3 = OrderItem(order_id=2, product_id=2, quantity=1, price_at_purchase=800.0)

    session.add_all([order_item1, order_item2, order_item3])


    review1 = Review(user_id=1, product_id=1, rating=5, comment="Excellent product!")
    review2 = Review(user_id=2, product_id=2, rating=4, comment="Very good but a bit pricey.")
    review3 = Review(user_id=1, product_id=3, rating=3, comment="Average quality.")

    session.add_all([review1, review2, review3])


    log1 = AuditLog(user_id=1, action="User logged in", timestamp=datetime.datetime.utcnow())
    log2 = AuditLog(user_id=1, action="Purchased Laptop", timestamp=datetime.datetime.utcnow())
    log3 = AuditLog(user_id=2, action="Reviewed Smartphone", timestamp=datetime.datetime.utcnow())

    session.add_all([log1, log2, log3])
    
    session.commit()
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    session.close()