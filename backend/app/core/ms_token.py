import os 
import msal 
import webbrowser
import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv

MS_GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'

def get_access_token(application_id, client_secret, scopes):
    client = msal.ConfidentialClientApplication(
        client_id=application_id,
        client_credential=client_secret,
        authority='https://login.microsoftonline.com/consumers/'
    )
    # Get the URL to open in the browser
    refresh_token=None
    refresh_token_path = Path('refresh_token.txt')
    if refresh_token_path.exists():
        with open(refresh_token_path, 'r') as f:
            refresh_token = f.read().strip()
    token_response = None
    if refresh_token:
        token_response = client.acquire_token_by_refresh_token(refresh_token, scopes)
    
    else:
        auth_request_uri = client.get_authorization_request_url(scopes)
        webbrowser.open(auth_request_uri)
        authorization_code = input('Paste the authorization code here: ')

        if not authorization_code:
            raise ValueError('Authorization code not provided')
        
        token_response = client.acquire_token_by_authorization_code(
            code=authorization_code,
            scopes=scopes
        )
    if 'access_token' in token_response:
        if 'refresh_token' in token_response:
            with open('refresh_token.txt', 'w') as f:
                f.write(token_response['refresh_token'])
        return token_response['access_token']
    else:
        raise Exception('Failed to acquire token'+str(token_response))

def main():
    load_dotenv()
    APPLICATION_ID = os.getenv('APPLICATION_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SCOPES  = ['User.Read', 'Mail.ReadWrite', 'Mail.Send']

    try:
        access_token = get_access_token(application_id=APPLICATION_ID, client_secret=CLIENT_SECRET, scopes=SCOPES)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        print(headers)
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()