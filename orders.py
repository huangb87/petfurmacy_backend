from flask import Blueprint, jsonify
import requests
from config import SHOPIFY_BASE_URL, SHOPIFY_AUTH

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    r = requests.get(f"{SHOPIFY_BASE_URL}/orders.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json().get('orders', []))
