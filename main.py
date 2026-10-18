import os
from typing import Any

import jwt
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="OAuth 2.0 / OIDC Token Verification Service", version="1.0.0")

ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-8h21cceg.apps.exam.local"

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2ok0HspNjgA+2rTLbeuY
cxiP/HG8C6Sb9iwg3yiLAA4HCnpITcbWCSelvbYGuC3EbNy4xFyf5Cbj5DHJMID
EkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXc
WyJjG2axVfmq7i6SuKr1JloWYG7xTTAvKPujS14otsQfO3h5NepzdfXpr28oNnzfW
ed+zc1R6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChdI19VDetJZVEgC5tkyvXsFI
SI6iyrYbKRONEBSqq4XKadejCsC4F1RncsS4L1gniT7GlkL9Mce3b0wGLs9/7ZIX
dQIDAQAB
-----END PUBLIC KEY-----"""

class VerifyRequest(BaseModel):
    token: str = Field(min_length=1)

@app.get("/")
def root() -> dict[str, str]:
    return {"service": "OAuth 2.0 / OIDC Token Verification Service", "endpoint": "POST /verify"}

@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}

@app.post("/verify")
def verify_token(body: VerifyRequest) -> dict[str, Any]:
    try:
        claims = jwt.decode(
            body.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iss": True,
                "verify_aud": True,
                "require": ["exp", "iss", "aud"],
            },
        )
        # The assignment requires the aud claim to equal the assigned audience,
        # not merely to contain it as one member of an array.
        if claims.get("aud") != AUDIENCE:
            return JSONResponse(status_code=401, content={"valid": False})
        return {
            "valid": True,
            "email": claims.get("email", ""),
            "sub": claims.get("sub", ""),
            "aud": claims.get("aud", ""),
        }
    except (jwt.InvalidTokenError, ValueError, TypeError):
        return JSONResponse(status_code=401, content={"valid": False})
