import requests
from decouple import config
import base64
import os
from dotenv import load_dotenv

class QuickbookAuth:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client_id = config('CLIENT_ID')
        self.client_secret = config('CLIENT_SECRET')
        self.refresh_token = config('REFRESH_TOKEN')
        self.redirect_url = config('REDIRECT_URL')
        self.realm_id = config('REALM_ID')
        self.access_token = config('ACCESS_TOKEN')

    def get_new_access_token(self):
        token_url = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
        }
        headers = {
            'Authorization': f'Basic {self._encode_credentials()}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            response = requests.post(token_url, data=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            print(f"Response Data: {data}")

            new_access_token = data.get('access_token')
            new_refresh_token = data.get('refresh_token')

            breakpoint()
            if new_access_token and new_refresh_token:
                self._update_token(new_access_token, new_refresh_token)
                return new_access_token

            raise Exception("Access token not found.")

        except requests.exceptions.RequestException as e:
            print(f"Error getting access token: {e}")
            if response:
                print(f"Response Content: {response.text}")
            return None

    def _update_token(self, new_access_token, new_refresh_token):
        load_dotenv()
        os.environ['ACCESS_TOKEN'] = new_access_token
        os.environ['REFRESH_TOKEN'] = new_refresh_token

        with open('.env', 'r') as file:
            lines = file.readlines()

        with open('.env', 'w') as file:
            for line in lines:
                if line.startswith('ACCESS_TOKEN'):
                    file.write(f"ACCESS_TOKEN={new_access_token}\n")
                elif line.startswith('REFRESH_TOKEN'):
                    file.write(f"REFRESH_TOKEN={new_refresh_token}\n")
                else:
                    file.write(line)


    def _encode_credentials(self):
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode()).decode()

