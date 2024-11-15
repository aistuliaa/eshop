# from sqlalchemy import func, extract
# from mod.model.idp_classes import Order, OrderItem, Product, Review
# from flask import Flask
# from sqlalchemy.orm import sessionmaker
# from mod.db.populate_db import engine
# from sqlalchemy.exc import SQLAlchemyError

# app = Flask(__name__)
# Session = sessionmaker(bind=engine)

# # Funkcijos
# def query_statistic(query_function):
#     """Bendra funkcija statistikoms vykdyti."""
#     session = Session()
#     try:
#         return query_function(session)
#     except SQLAlchemyError as e:
#         return {"error": str(e)}, 500
#     finally:
#         session.close()

# # Maršrutai
# @app.route('/stats/sales_per_day', methods=['GET'])
# def sales_per_day():
#     return query_statistic(lambda session: [
#         {"date": row[0].strftime("%Y-%m-%d"), "total_sold": row[1]}
#         for row in session.query(
#             Order.order_date,
#             func.sum(OrderItem.quantity).label('total_sold')
#         )
#         .join(OrderItem, Order.id == OrderItem.order_id)
#         .group_by(Order.order_date)
#         .all()
#     ])

# @app.route('/stats/revenue_per_day', methods=['GET'])
# def revenue_per_day():
#     return query_statistic(lambda session: [
#         {"date": row[0].strftime("%Y-%m-%d"), "total_revenue": row[1]}
#         for row in session.query(
#             Order.order_date,
#             func.sum(OrderItem.quantity * OrderItem.price_at_purchase).label('total_revenue')
#         )
#         .join(OrderItem, Order.id == OrderItem.order_id)
#         .group_by(Order.order_date)
#         .all()
#     ])

# @app.route('/stats/top_months', methods=['GET'])
# def top_months():
#     return query_statistic(lambda session: [
#         {"year": int(row[0]), "month": int(row[1]), "total_revenue": row[2]}
#         for row in session.query(
#             extract('year', Order.order_date).label('year'),
#             extract('month', Order.order_date).label('month'),
#             func.sum(OrderItem.quantity * OrderItem.price_at_purchase).label('total_revenue')
#         )
#         .join(OrderItem, Order.id == OrderItem.order_id)
#         .group_by("year", "month")
#         .order_by(func.sum(OrderItem.quantity * OrderItem.price_at_purchase).desc())
#         .all()
#     ])

# @app.route('/stats/top_rated_products', methods=['GET'])
# def top_rated_products():
#     return query_statistic(lambda session: [
#         {"product_name": row[0], "average_rating": round(row[1], 2)}
#         for row in session.query(
#             Product.name,
#             func.avg(Review.rating).label('average_rating')
#         )
#         .join(Review, Product.id == Review.product_id)
#         .group_by(Product.id)
#         .order_by(func.avg(Review.rating).desc())
#         .limit(5)
#         .all()
#     ])

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template
from mod.logger import setup_logger
from mod.model.idp_classes import Order, OrderItem, Product, Review
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, extract
from mod.db.populate_db import engine
from alembic import command
from alembic.config import Config

app = Flask(__name__)


logger = setup_logger()

Session = sessionmaker(bind=engine)
session = Session()


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")



@app.route('/templates/sales_per_day')
def sales_per_day():
    try:
        sales_data = session.query(
            Order.order_date,
            func.sum(OrderItem.quantity).label('total_sold')
        ).join(OrderItem, Order.id == OrderItem.order_id).group_by(Order.order_date).all()
        
        logger.info("successfully.")
        return render_template('sales_per_day.html', sales_data=sales_data)

    except Exception as e:
        logger.error(f"Error fetching sales per day: {e}")
        return "An error occurred", 500


@app.route('/templates/revenue_per_day')
def revenue_per_day():
    try:
        revenue_data = session.query(
            Order.order_date,
            func.sum(OrderItem.quantity * OrderItem.price_at_purchase).label('total_revenue')
        ).join(OrderItem, Order.id == OrderItem.order_id).group_by(Order.order_date).all()

        logger.info(" successfully.")
        return render_template('revenue_per_day.html', revenue_data=revenue_data)

    except Exception as e:
        logger.error(f"Error fetching revenue per day: {e}")
        return "An error occurred", 500


@app.route('/templates/top_months')
def top_months():
    try:
        months_data = session.query(
            extract('year', Order.order_date).label('year'),
            extract('month', Order.order_date).label('month'),
            func.sum(OrderItem.quantity * OrderItem.price_at_purchase).label('total_revenue')
        ).join(OrderItem, Order.id == OrderItem.order_id).group_by("year", "month").order_by(func.sum(OrderItem.quantity * OrderItem.price_at_purchase).desc()).all()

        logger.info("months statistics successfully.")
        return render_template('top_months.html', months_data=months_data)

    except Exception as e:
        logger.error(f"Error fetching top months: {e}")
        return "An error occurred", 500


@app.route('/stats/top_rated_products')
def top_rated_products():
    try:
        rated_products = session.query(
            Product.name,
            func.avg(Review.rating).label('average_rating')
        ).join(Review, Product.id == Review.product_id).group_by(Product.id).order_by(func.avg(Review.rating).desc()).limit(5).all()

        logger.info("Fetched top rated products successfully.")
        return render_template('top_rated_products.html', rated_products=rated_products)

    except Exception as e:
        logger.error(f"Error fetching top rated products: {e}")
        return "An error occurred", 500


if __name__ == '__main__':
  
    run_migrations()
    app.run(debug=True)