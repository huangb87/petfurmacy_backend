from flask import Blueprint, request, jsonify
from utils import storefront_graphql

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['POST'])
def create_cart():
    data = request.json or {}
    lines = data.get('lines', [])
    mutation = '''
    mutation cartCreate($input: CartInput!) {
      cartCreate(input: $input) {
        cart {
          id
          checkoutUrl
          lines(first: 10) {
            edges {
              node {
                id
                quantity
                merchandise {
                  ... on ProductVariant {
                    id
                    title
                  }
                }
              }
            }
          }
        }
        userErrors { field message }
      }
    }
    '''
    variables = {"input": {"lines": lines}}
    result = storefront_graphql(mutation, variables)
    return jsonify(result)

@cart_bp.route('/cart/<cart_id>', methods=['GET'])
def get_cart(cart_id):
    query = '''
    query getCart($id: ID!) {
      cart(id: $id) {
        id
        checkoutUrl
        lines(first: 10) {
          edges {
            node {
              id
              quantity
              merchandise {
                ... on ProductVariant {
                  id
                  title
                }
              }
            }
          }
        }
      }
    }
    '''
    variables = {"id": cart_id}
    result = storefront_graphql(query, variables)
    return jsonify(result)

@cart_bp.route('/cart/<cart_id>/add', methods=['POST'])
def add_to_cart(cart_id):
    data = request.json or {}
    lines = data.get('lines', [])
    mutation = '''
    mutation cartLinesAdd($cartId: ID!, $lines: [CartLineInput!]!) {
      cartLinesAdd(cartId: $cartId, lines: $lines) {
        cart {
          id
          checkoutUrl
          lines(first: 10) {
            edges {
              node {
                id
                quantity
                merchandise {
                  ... on ProductVariant {
                    id
                    title
                  }
                }
              }
            }
          }
        }
        userErrors { field message }
      }
    }
    '''
    variables = {"cartId": cart_id, "lines": lines}
    result = storefront_graphql(mutation, variables)
    return jsonify(result)

@cart_bp.route('/cart/<cart_id>/update', methods=['POST'])
def update_cart_line(cart_id):
    data = request.json or {}
    lines = data.get('lines', [])  # [{id: lineId, quantity: newQty}]
    mutation = '''
    mutation cartLinesUpdate($cartId: ID!, $lines: [CartLineUpdateInput!]!) {
      cartLinesUpdate(cartId: $cartId, lines: $lines) {
        cart {
          id
          checkoutUrl
          lines(first: 10) {
            edges {
              node {
                id
                quantity
                merchandise {
                  ... on ProductVariant {
                    id
                    title
                  }
                }
              }
            }
          }
        }
        userErrors { field message }
      }
    }
    '''
    variables = {"cartId": cart_id, "lines": lines}
    result = storefront_graphql(mutation, variables)
    return jsonify(result)

@cart_bp.route('/cart/<cart_id>/remove', methods=['POST'])
def remove_cart_lines(cart_id):
    data = request.json or {}
    line_ids = data.get('lineIds', [])
    mutation = '''
    mutation cartLinesRemove($cartId: ID!, $lineIds: [ID!]!) {
      cartLinesRemove(cartId: $cartId, lineIds: $lineIds) {
        cart {
          id
          checkoutUrl
          lines(first: 10) {
            edges {
              node {
                id
                quantity
                merchandise {
                  ... on ProductVariant {
                    id
                    title
                  }
                }
              }
            }
          }
        }
        userErrors { field message }
      }
    }
    '''
    variables = {"cartId": cart_id, "lineIds": line_ids}
    result = storefront_graphql(mutation, variables)
    return jsonify(result)

@cart_bp.route('/cart/<cart_id>/buyer', methods=['POST'])
def update_buyer_identity(cart_id):
    data = request.json or {}
    buyer_identity = data.get('buyerIdentity', {})
    mutation = '''
    mutation cartBuyerIdentityUpdate($cartId: ID!, $buyerIdentity: CartBuyerIdentityInput!) {
      cartBuyerIdentityUpdate(cartId: $cartId, buyerIdentity: $buyerIdentity) {
        cart {
          id
          buyerIdentity {
            email
            phone
            countryCode
            customer {
              id
              displayName
            }
          }
        }
        userErrors { field message }
      }
    }
    '''
    variables = {"cartId": cart_id, "buyerIdentity": buyer_identity}
    result = storefront_graphql(mutation, variables)
    return jsonify(result)

@cart_bp.route('/cart/<cart_id>/shipping', methods=['POST'])
def update_shipping_address(cart_id):
    data = request.json or {}
    shipping_address = data.get('shippingAddress', {})
    mutation = '''
    mutation cartShippingAddressUpdate($cartId: ID!, $shippingAddress: MailingAddressInput!) {
      cartShippingAddressUpdate(cartId: $cartId, shippingAddress: $shippingAddress) {
        cart {
          id
          shippingAddress {
            address1
            address2
            city
            province
            country
            zip
          }
        }
        userErrors { field message }
      }
    }
    '''
    variables = {"cartId": cart_id, "shippingAddress": shipping_address}
    result = storefront_graphql(mutation, variables)
    return jsonify(result)

@cart_bp.route('/checkout', methods=['POST'])
def checkout():
    cart_id = request.json.get('cart_id')
    query = '''
    query getCart($id: ID!) {
      cart(id: $id) {
        checkoutUrl
      }
    }
    '''
    variables = {"id": cart_id}
    result = storefront_graphql(query, variables)
    checkout_url = result.get('data', {}).get('cart', {}).get('checkoutUrl')
    return jsonify({'checkoutUrl': checkout_url})
