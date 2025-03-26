
---

# Setup Guide

This guide provides simple instructions to set up the OAuth2 PKCE Flow application on your local machine.

## Prerequisites

1. **Python 3.6+**  
   Ensure Python is installed. You can check by running:
   ```bash
   python --version
   ```
   If not installed, download it from [python.org](https://www.python.org/downloads/).

2. **pip** (Python package manager)  
   Ensure `pip` is installed by running:
   ```bash
   pip --version
   ```
   If it's not installed, follow [this guide](https://pip.pypa.io/en/stable/installation/) to set it up.

3. **OAuth Provider Account** (e.g., Auth0)  
   Set up an OAuth application to get your **Domain**, **Client ID**, **Client Secret**, and **Redirect URI**.

## Required Dependencies

Make sure to install the following dependencies. You can create a `requirements.txt` file with these packages:

```
Flask==2.0.2
python-dotenv==3.13.1
requests==2.26.0
PyJWT==2.1.0
```

Alternatively, you can install them directly using `pip`:

```bash
pip install Flask python-dotenv requests PyJWT
```

## Installation Steps

1. **Pull the repository to a local environment**.

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Setup

1. **Create a `.env` file** in the root directory of the project:
   ```bash
   touch .env
   ```

2. **Add your OAuth credentials** to the `.env` file:
   ```bash
   DOMAIN=your-oauth-domain
   CLIENT_ID=your-client-id
   CLIENT_SECRET=your-client-secret
   REDIRECT_URI=http://localhost:5000/callback
   ```

## Running the Application

1. **Start the Flask development server**:
   ```bash
   python llm_api_app.py
   ```

2. **Access the application** in your web browser:
   ```
   http://localhost:5000
   ```

3. **Authenticate via OAuth**: You will be redirected to the OAuth provider's login page for authentication.

4. **View the tokens**: After authentication, the access token and decoded JWT payload will be displayed.

---
