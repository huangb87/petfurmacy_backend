import requests
from config import SHOPIFY_STOREFRONT_URL, SHOPIFY_STOREFRONT_ACCESS_TOKEN

def storefront_graphql(query, variables=None):
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Storefront-Access-Token": SHOPIFY_STOREFRONT_ACCESS_TOKEN,
    }
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = requests.post(SHOPIFY_STOREFRONT_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
