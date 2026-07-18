import jwt
import os
from urllib.parse import parse_qs
from dotenv import load_dotenv
from channels.db import database_sync_to_async

load_dotenv()


@database_sync_to_async
def get_user_from_token(token):
    try:
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=["HS256"]
        )

        user_type = payload.get("type")

        if user_type == "donor":
            from users.models import Donor
            return Donor.objects.get(id=payload["id"])

        elif user_type == "partner":
            from partners.models import Partners
            return Partners.objects.get(id=payload["id"])

    except Exception:
        return None

    return None


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())

        token = query_string.get("token")

        if token:
            scope["user"] = await get_user_from_token(token[0])
        else:
            scope["user"] = None

        return await self.app(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)