from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

customers_bp = Blueprint('customers', __name__)

# In-memory store for demo purposes
CUSTOMERS = {}

# Helper for login required
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'customer_email' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated

@customers_bp.route('/customers/register', methods=['POST'])
def register_customer():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name', '')
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    if email in CUSTOMERS:
        return jsonify({'error': 'Customer already exists'}), 409
    CUSTOMERS[email] = {
        'email': email,
        'password_hash': generate_password_hash(password),
        'name': name,
        'addresses': []
    }
    return jsonify({'message': 'Customer registered successfully'})

@customers_bp.route('/customers/login', methods=['POST'])
def login_customer():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    customer = CUSTOMERS.get(email)
    if not customer or not check_password_hash(customer['password_hash'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    session['customer_email'] = email
    return jsonify({'message': 'Logged in successfully'})

@customers_bp.route('/customers/logout', methods=['POST'])
@login_required
def logout_customer():
    session.pop('customer_email', None)
    return jsonify({'message': 'Logged out successfully'})

@customers_bp.route('/customers/profile', methods=['GET'])
@login_required
def get_profile():
    email = session['customer_email']
    customer = CUSTOMERS[email].copy()
    customer.pop('password_hash')
    return jsonify(customer)

@customers_bp.route('/customers/profile', methods=['PUT'])
@login_required
def update_profile():
    email = session['customer_email']
    data = request.json
    name = data.get('name')
    if name:
        CUSTOMERS[email]['name'] = name
    return jsonify({'message': 'Profile updated'})

@customers_bp.route('/customers/password', methods=['PUT'])
@login_required
def update_password():
    email = session['customer_email']
    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    customer = CUSTOMERS[email]
    if not check_password_hash(customer['password_hash'], old_password):
        return jsonify({'error': 'Old password incorrect'}), 400
    customer['password_hash'] = generate_password_hash(new_password)
    return jsonify({'message': 'Password updated'})

# Address management
@customers_bp.route('/customers/addresses', methods=['GET'])
@login_required
def get_addresses():
    email = session['customer_email']
    return jsonify(CUSTOMERS[email]['addresses'])

@customers_bp.route('/customers/addresses', methods=['POST'])
@login_required
def add_address():
    email = session['customer_email']
    address = request.json
    CUSTOMERS[email]['addresses'].append(address)
    return jsonify({'message': 'Address added'})

@customers_bp.route('/customers/addresses/<int:idx>', methods=['PUT'])
@login_required
def update_address(idx):
    email = session['customer_email']
    address = request.json
    if idx < 0 or idx >= len(CUSTOMERS[email]['addresses']):
        return jsonify({'error': 'Address not found'}), 404
    CUSTOMERS[email]['addresses'][idx] = address
    return jsonify({'message': 'Address updated'})

@customers_bp.route('/customers/addresses/<int:idx>', methods=['DELETE'])
@login_required
def delete_address(idx):
    email = session['customer_email']
    if idx < 0 or idx >= len(CUSTOMERS[email]['addresses']):
        return jsonify({'error': 'Address not found'}), 404
    CUSTOMERS[email]['addresses'].pop(idx)
    return jsonify({'message': 'Address deleted'})
