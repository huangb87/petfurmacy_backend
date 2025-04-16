from flask import Blueprint, jsonify
import requests
from config import SHOPIFY_BASE_URL, SHOPIFY_AUTH

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    r = requests.get(f"{SHOPIFY_BASE_URL}/products.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json().get('products', []))

@products_bp.route('/products/<product_id>', methods=['GET'])
def get_product_detail(product_id):
    r = requests.get(f"{SHOPIFY_BASE_URL}/products/{product_id}.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json().get('product', {}))

@products_bp.route('/collections', methods=['GET'])
def get_collections():
    r = requests.get(f"{SHOPIFY_BASE_URL}/custom_collections.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json().get('custom_collections', []))
