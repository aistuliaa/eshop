from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///mod/db/duombaze.db', echo=True)

# Set up a session factory
Session = sessionmaker(bind=engine)
session = Session()