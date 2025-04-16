import os
from flask import Flask
from flask_cors import CORS
from config import *
from products import products_bp
from orders import orders_bp
from cart import cart_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(cart_bp)

if __name__ == '__main__':
    app.run(debug=True)
