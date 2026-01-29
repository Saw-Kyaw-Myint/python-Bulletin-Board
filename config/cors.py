"""
config/cors.py

Cross-Origin Resource Sharing (CORS) configuration for the Flask application.

CORS_CONFIG defines which origins, methods, and headers are allowed
for cross-origin requests. It also specifies whether credentials
(e.g., cookies, Authorization headers) are supported.

Configuration:
    - origins (List[str]): List of allowed origins for requests.
      Example: ["http://localhost:3000"]
    - methods (List[str]): HTTP methods allowed for cross-origin requests.
      Example: ["GET", "POST", "PUT", "DELETE"]
    - allow_headers (List[str]): Allowed headers in requests.
      Example: ["Content-Type", "Authorization"]
    - supports_credentials (bool): Whether cookies and credentials are allowed.
"""

import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# CORS configuration dictionary
CORS_CONFIG = {
    "origins": [os.environ.get("FRONTEND_URL", "http://localhost:5173")],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization", "X-Refresh-Token"],
}
