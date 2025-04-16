from flask import Blueprint, request, jsonify
import requests
from config import SHOPIFY_BASE_URL, SHOPIFY_AUTH
from utils import storefront_graphql
from products import admin_required

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    # Optional: support filters via query args
    params = {}
    status = request.args.get('status')
    if status:
        params['status'] = status
    customer_id = request.args.get('customer_id')
    if customer_id:
        params['customer_id'] = customer_id
    r = requests.get(f"{SHOPIFY_BASE_URL}/orders.json", auth=SHOPIFY_AUTH, params=params)
    return jsonify(r.json().get('orders', []))

@orders_bp.route('/orders/<order_id>', methods=['GET'])
def get_order_detail(order_id):
    r = requests.get(f"{SHOPIFY_BASE_URL}/orders/{order_id}.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json().get('order', {}))

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    # See Shopify Admin API docs for order creation format
    order_data = request.json
    r = requests.post(f"{SHOPIFY_BASE_URL}/orders.json", auth=SHOPIFY_AUTH, json={'order': order_data})
    return jsonify(r.json())

@orders_bp.route('/orders/<order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    r = requests.post(f"{SHOPIFY_BASE_URL}/orders/{order_id}/cancel.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json())

@orders_bp.route('/orders/<order_id>/fulfillment', methods=['GET'])
def get_fulfillment(order_id):
    r = requests.get(f"{SHOPIFY_BASE_URL}/orders/{order_id}/fulfillments.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json().get('fulfillments', []))

# --- Customer-facing endpoints (Storefront API) ---
@orders_bp.route('/customer/orders', methods=['POST'])
def customer_orders():
    data = request.json or {}
    customer_access_token = data.get('accessToken')
    query = '''
    query customerOrders($customerAccessToken: String!) {
      customer(customerAccessToken: $customerAccessToken) {
        orders(first: 10, reverse: true) {
          edges {
            node {
              id
              name
              orderNumber
              processedAt
              fulfillmentStatus
              financialStatus
              totalPriceSet { shopMoney { amount currencyCode } }
              lineItems(first: 20) {
                edges {
                  node {
                    title
                    quantity
                  }
                }
              }
            }
          }
        }
      }
    }
    '''
    variables = {"customerAccessToken": customer_access_token}
    result = storefront_graphql(query, variables)
    return jsonify(result)

@orders_bp.route('/customer/orders/<order_id>', methods=['POST'])
def customer_order_detail(order_id):
    data = request.json or {}
    customer_access_token = data.get('accessToken')
    query = '''
    query customerOrder($customerAccessToken: String!, $orderId: ID!) {
      customer(customerAccessToken: $customerAccessToken) {
        order(id: $orderId) {
          id
          name
          orderNumber
          processedAt
          fulfillmentStatus
          financialStatus
          totalPriceSet { shopMoney { amount currencyCode } }
          lineItems(first: 20) {
            edges {
              node {
                title
                quantity
              }
            }
          }
        }
      }
    }
    '''
    variables = {"customerAccessToken": customer_access_token, "orderId": order_id}
    result = storefront_graphql(query, variables)
    return jsonify(result)

# --- Order update (Admin API) ---
@orders_bp.route('/orders/<order_id>/update', methods=['POST'])
def update_order(order_id):
    update_data = request.json or {}
    r = requests.put(f"{SHOPIFY_BASE_URL}/orders/{order_id}.json", auth=SHOPIFY_AUTH, json={'order': update_data})
    return jsonify(r.json())

# --- Fulfillment Management (Admin API) ---
@orders_bp.route('/orders/<order_id>/fulfillments', methods=['POST'])
@admin_required
def create_fulfillment(order_id):
    data = request.json or {}
    r = requests.post(f"{SHOPIFY_BASE_URL}/orders/{order_id}/fulfillments.json", auth=SHOPIFY_AUTH, json={'fulfillment': data})
    return jsonify(r.json()), r.status_code

@orders_bp.route('/orders/<order_id>/fulfillments/<fulfillment_id>', methods=['PUT'])
@admin_required
def update_fulfillment(order_id, fulfillment_id):
    data = request.json or {}
    r = requests.put(f"{SHOPIFY_BASE_URL}/orders/{order_id}/fulfillments/{fulfillment_id}.json", auth=SHOPIFY_AUTH, json={'fulfillment': data})
    return jsonify(r.json()), r.status_code

@orders_bp.route('/orders/<order_id>/fulfillments/<fulfillment_id>/cancel', methods=['POST'])
@admin_required
def cancel_fulfillment(order_id, fulfillment_id):
    r = requests.post(f"{SHOPIFY_BASE_URL}/orders/{order_id}/fulfillments/{fulfillment_id}/cancel.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json()), r.status_code

@orders_bp.route('/orders/<order_id>/fulfillments/<fulfillment_id>', methods=['GET'])
@admin_required
def get_fulfillment_detail(order_id, fulfillment_id):
    r = requests.get(f"{SHOPIFY_BASE_URL}/orders/{order_id}/fulfillments/{fulfillment_id}.json", auth=SHOPIFY_AUTH)
    return jsonify(r.json().get('fulfillment', {})), r.status_code
