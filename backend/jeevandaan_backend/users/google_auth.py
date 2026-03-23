from google.oauth2 import id_token
from google.auth.transport import requests
import os
from dotenv import load_dotenv

load_dotenv()


def verify_google_token(token):
    """
    Verify Google token and return user info
    """
    try:
        # Verify token with Google
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            os.getenv('GOOGLE_CLIENT_ID')
        )

        # Token is valid — extract user info
        return {
            'google_id': idinfo['sub'],
            'email': idinfo['email'],
            'name': idinfo['name'],
            'profile_photo': idinfo.get('picture', ''),
        }

    except Exception as e:
        print(f"Google token verification failed: {str(e)}")
        return None