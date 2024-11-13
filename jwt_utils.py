import jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Function to create a new access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    print(ALGORITHM,SECRET_KEY)
    print("Input token:", token)
    try:
        # Decode the primary token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Primary payload decoded:", payload)

        # Check for a nested token inside `access_token`
        if "access_token" in payload:
            print("Nested token found in `access_token`. Decoding it...")
            nested_payload = jwt.decode(payload["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
            print("Nested payload decoded:", nested_payload)
            return nested_payload  # Return the nested payload
        return payload  # Return the primary payload if no nested token

    except jwt.ExpiredSignatureError:
        print("Error: Token has expired.")
        return None

    except jwt.InvalidTokenError as e:
        print(f"Error: Invalid token - {str(e)}")
        return None

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None


# Pydantic model to parse the token payload
class TokenData(BaseModel):
    username: str
