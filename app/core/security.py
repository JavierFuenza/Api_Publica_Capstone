"""
Firebase authentication and security utilities.
"""

import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os

from app.core.config import settings

# Initialize Firebase Admin SDK
_firebase_initialized = False


def initialize_firebase():
    """Initialize Firebase Admin SDK with credentials."""
    global _firebase_initialized

    if _firebase_initialized:
        return

    try:
        # Check if credentials file exists
        if not os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
            print(f"WARNING: Firebase credentials file not found at {settings.FIREBASE_CREDENTIALS_PATH}")
            print("Firebase authentication will not work until you add the credentials file.")
            return

        # Initialize Firebase
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        print("Firebase Admin SDK initialized successfully")

    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        print("Firebase authentication will not work.")


# HTTP Bearer token security
security = HTTPBearer()


class FirebaseUser:
    """Represents an authenticated Firebase user."""

    def __init__(self, uid: str, email: Optional[str] = None, claims: dict = None):
        self.uid = uid
        self.email = email
        self.claims = claims or {}

    def __repr__(self):
        return f"<FirebaseUser(uid={self.uid}, email={self.email})>"


async def verify_firebase_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> FirebaseUser:
    """
    Verify Firebase ID token and return user information.

    Args:
        credentials: HTTP Authorization credentials with Bearer token

    Returns:
        FirebaseUser: Authenticated user information

    Raises:
        HTTPException: If token is invalid or expired
    """
    if not _firebase_initialized:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Firebase authentication is not configured. Please contact administrator."
        )

    token = credentials.credentials

    try:
        # Verify the token
        decoded_token = auth.verify_id_token(token)

        # Extract user information
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")

        if not uid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )

        return FirebaseUser(uid=uid, email=email, claims=decoded_token)

    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired"
        )
    except auth.RevokedIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has been revoked"
        )
    except auth.CertificateFetchError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to verify token. Please try again later."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )


async def get_current_user(
    user: FirebaseUser = Security(verify_firebase_token)
) -> FirebaseUser:
    """
    Dependency to get the current authenticated user.

    Usage:
        @app.get("/protected")
        async def protected_route(user: FirebaseUser = Depends(get_current_user)):
            return {"message": f"Hello {user.email}"}
    """
    return user


# OPTIONAL: For testing without Firebase authentication
async def get_current_user_optional() -> Optional[FirebaseUser]:
    """
    Optional authentication - returns None if not authenticated.
    Use this for testing without Firebase credentials.

    To enable test mode, set FIREBASE_TEST_MODE=true in .env
    """
    # Check if test mode is enabled
    test_mode = os.getenv("FIREBASE_TEST_MODE", "false").lower() == "true"

    if test_mode:
        print("⚠️  TEST MODE: Authentication disabled")
        return FirebaseUser(uid="test-user", email="test@example.com")

    # In production, this would require real authentication
    if not _firebase_initialized:
        return FirebaseUser(uid="test-user", email="test@example.com")

    return None
