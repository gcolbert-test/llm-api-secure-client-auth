# OAuth2 PKCE Flow Application

This is a simple Python application that demonstrates the OAuth2 Authorization Code Grant Flow with Proof Key for Code Exchange (PKCE) for an internal LLM application. The application is built using Flask, `requests`, and `PyJWT` for OAuth2 authentication.

## Features

- OAuth2 Authorization Code Grant Flow with PKCE
- User authentication and authorization using an external OAuth provider
- JWT decoding to extract user information

## Requirements

- Python 3
- `pip` for package management

## Setup

To get the application up and running, follow the instructions in the [Setup Guide](SiriusSetupGiude.md).

## Usage

1. Start the Flask development server by running the following command:

   ```bash
   python llm_api_app.py
