import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

SHOPIFY_STORE_DOMAIN = os.environ.get('SHOPIFY_STORE_DOMAIN', 'yourstore.myshopify.com')
SHOPIFY_API_KEY = os.environ.get('SHOPIFY_API_KEY', 'your_api_key')
SHOPIFY_API_PASSWORD = os.environ.get('SHOPIFY_API_PASSWORD', 'your_api_password')
SHOPIFY_API_VERSION = '2023-04'

# Helper for Shopify Admin API auth
SHOPIFY_AUTH = (SHOPIFY_API_KEY, SHOPIFY_API_PASSWORD)
SHOPIFY_BASE_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}"

@app.route('/products', methods=['GET'])
def get_products():
    """Fetch products from Shopify"""
    r = requests.get(f"{SHOPIFY_BASE_URL}/products.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json().get('products', []))

@app.route('/products/<product_id>', methods=['GET'])
def get_product_detail(product_id):
    r = requests.get(f"{SHOPIFY_BASE_URL}/products/{product_id}.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json().get('product', {}))

@app.route('/collections', methods=['GET'])
def get_collections():
    r = requests.get(f"{SHOPIFY_BASE_URL}/custom_collections.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json().get('custom_collections', []))

@app.route('/cart', methods=['POST'])
def create_cart():
    # For demonstration: just echo back the cart data
    # In production, you may want to use Shopify's Storefront API for cart/checkout
    cart_data = request.json
    return jsonify({"cart": cart_data, "msg": "Cart received (simulate)"})

@app.route('/checkout', methods=['POST'])
def checkout():
    # In production, use Shopify's checkout API or Storefront API
    checkout_data = request.json
    # Simulate order creation
    return jsonify({"order": checkout_data, "msg": "Order placed (simulate)"})

@app.route('/orders', methods=['GET'])
def get_orders():
    r = requests.get(f"{SHOPIFY_BASE_URL}/orders.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json().get('orders', []))

if __name__ == '__main__':
    app.run(debug=True)
