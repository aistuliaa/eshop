from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, create_engine
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///mod/db/duombaze.db', echo=False)
Base = declarative_base()

current_time = datetime.utcnow
# Vartotojas

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Nepamisti hasuoti
    balance = Column(Float, default=0.0)
    is_blocked = Column(Boolean, default=False)     # True/False
    failed_logins = Column(Integer, default=0)      # Tam, kad duoti 5min blokavima
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String(20), default='customer')   # admin/customer


# Produkats

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False) # kiekis
    category = Column(String(50)) # galimai galima apseiti be kategorijos
    rating = Column(Float, default=0.0)


# Vezimelis

class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

# Uzsakimai

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='completed') # pending/completed



# vartotojo įgūdžių zenkliukai

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)


# Ivertinimas

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    rating = Column(Integer, nullable=False)  # Nuo 1-5
    comment = Column(String(500))
    review_date = Column(DateTime, default=datetime.utcnow)


# prisijungimas prie užsiėmimų

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)
