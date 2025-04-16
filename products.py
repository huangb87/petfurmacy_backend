from flask import Blueprint, jsonify, request, session
import requests
from config import SHOPIFY_BASE_URL, SHOPIFY_AUTH

products_bp = Blueprint('products', __name__)

# --- Admin check helper ---
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        # Simple admin check: session['is_admin'] must be True
        if not session.get('is_admin', False):
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated

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

# --- Create product ---
@products_bp.route('/products', methods=['POST'])
@admin_required
def create_product():
    data = request.json
    r = requests.post(f"{SHOPIFY_BASE_URL}/products.json", json={'product': data}, auth=SHOPIFY_AUTH)
    return jsonify(r.json()), r.status_code

# --- Update product ---
@products_bp.route('/products/<product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    data = request.json
    r = requests.put(f"{SHOPIFY_BASE_URL}/products/{product_id}.json", json={'product': data}, auth=SHOPIFY_AUTH)
    return jsonify(r.json()), r.status_code

# --- Delete product ---
@products_bp.route('/products/<product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    r = requests.delete(f"{SHOPIFY_BASE_URL}/products/{product_id}.json", auth=SHOPIFY_AUTH)
    return jsonify({'deleted': r.status_code == 200}), r.status_code

# --- Variant management ---
@products_bp.route('/products/<product_id>/variants', methods=['POST'])
@admin_required
def create_variant(product_id):
    data = request.json
    r = requests.post(f"{SHOPIFY_BASE_URL}/products/{product_id}/variants.json", json={'variant': data}, auth=SHOPIFY_AUTH)
    return jsonify(r.json()), r.status_code

@products_bp.route('/variants/<variant_id>', methods=['PUT'])
@admin_required
def update_variant(variant_id):
    data = request.json
    r = requests.put(f"{SHOPIFY_BASE_URL}/variants/{variant_id}.json", json={'variant': data}, auth=SHOPIFY_AUTH)
    return jsonify(r.json()), r.status_code

@products_bp.route('/variants/<variant_id>', methods=['DELETE'])
@admin_required
def delete_variant(variant_id):
    r = requests.delete(f"{SHOPIFY_BASE_URL}/variants/{variant_id}.json", auth=SHOPIFY_AUTH)
    return jsonify({'deleted': r.status_code == 200}), r.status_code

# --- Inventory update ---
@products_bp.route('/inventory_levels/<inventory_item_id>', methods=['PUT'])
@admin_required
def update_inventory(inventory_item_id):
    data = request.json
    available = data.get('available')
    location_id = data.get('location_id')
    if available is None or not location_id:
        return jsonify({'error': 'available and location_id required'}), 400
    payload = {
        'location_id': location_id,
        'inventory_item_id': inventory_item_id,
        'available': available
    }
    r = requests.post(f"{SHOPIFY_BASE_URL}/inventory_levels/set.json", json=payload, auth=SHOPIFY_AUTH)
    return jsonify(r.json()), r.status_code

# --- Product images, tags, metafields ---
@products_bp.route('/products/<product_id>/images', methods=['GET'])
def get_product_images(product_id):
    r = requests.get(f"{SHOPIFY_BASE_URL}/products/{product_id}/images.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json().get('images', []))

@products_bp.route('/products/<product_id>/tags', methods=['GET'])
def get_product_tags(product_id):
    r = requests.get(f"{SHOPIFY_BASE_URL}/products/{product_id}.json", auth=SHOPIFY_AUTH)
    product = r.json().get('product', {})
    tags = product.get('tags', '')
    return jsonify(tags.split(',') if tags else [])

@products_bp.route('/products/<product_id>/metafields', methods=['GET'])
def get_product_metafields(product_id):
    r = requests.get(f"{SHOPIFY_BASE_URL}/products/{product_id}/metafields.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json().get('metafields', []))
