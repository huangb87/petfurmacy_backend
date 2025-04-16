import os
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_STORE_DOMAIN = os.environ.get('SHOPIFY_STORE_DOMAIN', 'yourstore.myshopify.com')
SHOPIFY_API_KEY = os.environ.get('SHOPIFY_API_KEY', 'your_api_key')
SHOPIFY_API_PASSWORD = os.environ.get('SHOPIFY_API_PASSWORD', 'your_api_password')
SHOPIFY_API_VERSION = '2023-04'
SHOPIFY_AUTH = (SHOPIFY_API_KEY, SHOPIFY_API_PASSWORD)
SHOPIFY_BASE_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}"

# Storefront API
SHOPIFY_STOREFRONT_ACCESS_TOKEN = os.environ.get('SHOPIFY_STOREFRONT_ACCESS_TOKEN', 'your_storefront_token')
SHOPIFY_STOREFRONT_URL = f"https://{SHOPIFY_STORE_DOMAIN}/api/2023-04/graphql.json"
