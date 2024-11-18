from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    balance = Column(Float, default=0.0)
    is_blocked = Column(Boolean, default=False)
    failed_logins = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String(20), default='customer')

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return str(self.id)
    
    @property
    def is_active(self):
        return not self.is_blocked

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def block_user(self):
        self.is_blocked = True
        self.failed_logins = 0

    def reset_failed_logins(self):
        self.failed_logins = 0

    def increment_failed_logins(self):
        self.failed_logins += 1

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String(50))
    rating = Column(Float, default=0.0)

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price})>"

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='audit_logs')

User.audit_logs = relationship('AuditLog', back_populates='user')

db_directory = os.path.join(os.path.dirname(__file__), '..', 'db')
os.makedirs(db_directory, exist_ok=True)
db_path = os.path.join(db_directory, 'duombaze.db')
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, echo=True)

if not os.path.exists(db_path):
    Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

def seed_users():
    """Function to seed the database with a test user."""
    try:
        existing_user = session.query(User).filter_by(username="testuser").first()
        if not existing_user:
            test_user = User(
                username="testuser",
                email="testuser@example.com",
                password=generate_password_hash("password123", method='pbkdf2:sha256', salt_length=16),
                role="customer"
            )
            session.add(test_user)
            session.commit()
            print("Test user added successfully.")
        else:
            print("Test user already exists.")
    except Exception as e:
        session.rollback()
        print(f"Error seeding users: {e}")


def log_action(user_id, action):
    """Log a specific user action."""
    try:
        log_entry = AuditLog(user_id=user_id, action=action)
        session.add(log_entry)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error logging action: {e}")


if __name__ == "__main__":
    seed_users()