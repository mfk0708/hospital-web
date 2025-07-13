from fastapi import Header, HTTPException, status
import os

def verify_api_key(x_api_key: str = Header(...)):
    expected_api_key = os.getenv("API_KEY")
    print("Expected key:", expected_api_key)
    print("Received key:", x_api_key)
    
    if x_api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    
