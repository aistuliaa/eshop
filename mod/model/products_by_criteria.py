from flask import Flask, render_template, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, func
from mod.model.idp_classes import engine, Product, Review, OrderItem

app = Flask(__name__)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/products', methods=['GET'])
def view_products():
    sort_option = request.args.get('sort', 'price')  
    products = []

    try:
        
        if sort_option == 'price':
            products = session.query(Product).order_by(Product.price).all()
        elif sort_option == 'rating':
            # Rusiavimas/filtravimas
            products = session.query(Product).outerjoin(Review).group_by(Product.id) \
                .order_by(desc(func.avg(Review.rating))).all() # apskaiciuoja ivertinimo vidurki avg
        elif sort_option == 'delivery_date':
         
            products = session.query(Product).outerjoin(OrderItem).group_by(Product.id) \
                .order_by(desc(func.max(OrderItem.order_date))).all() #pagal pristatymo data, surusiuos datas mazejimo tvarka
        elif sort_option == 'bestsellers':
           
            products = session.query(Product).outerjoin(OrderItem).group_by(Product.id) \
                .order_by(desc(func.count(OrderItem.product_id))).all()
        else:
            products = session.query(Product).all()

        if not products:
            error_message = "No products found."
            return render_template("error.html", error=error_message)
        
        return render_template("products.html", products=products, sort_option=sort_option)

    except Exception as e:
        error_message = f"An error: {str(e)}"
        return render_template("error.html", error=error_message)

if __name__ == '__main__':
    app.run(debug=True)