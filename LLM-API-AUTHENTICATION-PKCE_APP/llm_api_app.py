import os
import base64
import hashlib
import secrets
import requests
import jwt  # Import PyJWT
from flask import Flask, redirect, request, session, jsonify 
from dotenv import load_dotenv  # Import the load_dotenv function

# Load the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# OAuth2 configurations (these values are now loaded from the .env file)
DOMAIN = os.getenv('DOMAIN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
AUTHORIZATION_URL = f'https://{DOMAIN}/authorize'
TOKEN_URL = f'https://{DOMAIN}/oauth/token'

# Generate PKCE code verifier and challenge
def generate_pkce_pair():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8').rstrip('=')
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').rstrip('=')
    return code_verifier, code_challenge

@app.route('/')
def index():
    # Start the OAuth2 flow
    code_verifier, code_challenge = generate_pkce_pair()
    session['code_verifier'] = code_verifier

    # Redirect to the authorization URL
    authorization_redirect_url = (
        f'{AUTHORIZATION_URL}?response_type=code&client_id={CLIENT_ID}'
        f'&redirect_uri={REDIRECT_URI}&scope=openid%20profile%20email'  # Include openid scope
        f'&code_challenge={code_challenge}&code_challenge_method=S256'
    )
    return redirect(authorization_redirect_url)

@app.route('/callback')
def callback():
    # Get authorization code from the callback request
    authorization_code = request.args.get('code')
    if not authorization_code:
        return 'Authorization failed. No code provided.', 400

    # Exchange authorization code for an access token
    code_verifier = session.pop('code_verifier', None)
    if not code_verifier:
        return 'PKCE code verifier missing from session.', 400

    token_response = requests.post(
        TOKEN_URL,
        data={
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': authorization_code,
            'redirect_uri': REDIRECT_URI,
            'code_verifier': code_verifier
        }
    )

    # Print detailed response to understand the error
    print(f"Status Code: {token_response.status_code}")
    print(f"Response Text: {token_response.text}")

    if token_response.status_code != 200:
        return f'Token exchange failed: {token_response.text}', token_response.status_code

    # Retrieve access token and id token if present
    token_data = token_response.json()
    access_token = token_data.get('access_token')
    id_token = token_data.get('id_token')

    # Skip decoding the access token since it might be opaque
    decoded_access_token = "Access token is opaque and cannot be decoded"

    if id_token:
        # Decode the id_token (JWT)
        id_token_payload = jwt.decode(id_token, options={"verify_signature": False})
        return jsonify({
            'access_token': access_token,
            'access_token_message': decoded_access_token,  # Inform about opaque token
            'id_token_payload': id_token_payload  # Display decoded id_token
        })
    else:
        # Return the access token if id_token is not present
        return jsonify({
            'access_token': access_token,
            'access_token_message': decoded_access_token,  # Inform about opaque token
            'message': 'ID token not provided in response.'
        })

if __name__ == '__main__':
    # Use app.run() to run the Flask app for local development
    app.run(host='localhost', port=5000, debug=True)
