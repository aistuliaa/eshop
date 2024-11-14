from flask import Flask, render_template
from sqlalchemy.orm import sessionmaker
from idp_classes import engine, Product

app = Flask(__name__)


Session = sessionmaker(bind=engine)
session = Session()

@app.route('/products', methods=['GET'])
def view_products():
    try:
        products = session.query(Product).all()
        if not products:
            error_message = "No products found."
            return render_template("error.html", error=error_message)
        return render_template("products.html", products=products)
    except Exception as e:
        error_message = f"An error occurred while fetching products: {str(e)}"
        return render_template("error.html", error=error_message)

if __name__ == '__main__':
    app.run(debug=True)