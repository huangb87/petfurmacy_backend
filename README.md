# Pet Furmacy Mini Program Backend (Flask)

This backend provides API endpoints for your WeChat Mini Program to communicate with your Shopify store securely.

## Setup

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Set environment variables for your Shopify store:
   - `SHOPIFY_STORE_DOMAIN` (e.g. yourstore.myshopify.com)
   - `SHOPIFY_API_KEY` (from Shopify Admin/private app)
   - `SHOPIFY_API_PASSWORD` (from Shopify Admin/private app)
3. Run the backend:
   ```sh
   python app.py
   ```

## Endpoints
- `GET /products` — List products
- `GET /products/<id>` — Product detail
- `GET /collections` — List collections
- `POST /cart` — Simulate cart creation/update
- `POST /checkout` — Simulate order placement
- `GET /orders` — List orders

## Notes
- All Shopify credentials are kept server-side for security.
- The Mini Program frontend should call these endpoints, not Shopify directly.
- For production, implement authentication and HTTPS.
