# OAuth 2.0 / OIDC Token Verification Service

FastAPI service implementing `POST /verify` for the assignment.

## Deploy to Render
1. Push these files to a GitHub repository.
2. In Render, choose **New + → Web Service** and connect the repository.
3. Render can use `render.yaml`; otherwise set build command to `pip install -r requirements.txt` and start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`.
4. Deploy and submit the full endpoint URL, e.g. `https://YOUR-SERVICE.onrender.com/verify`.

## Request
```http
POST /verify
Content-Type: application/json

{"token":"<JWT string>"}
```

Valid tokens produce HTTP 200 with `valid: true` and the `email`, `sub`, and `aud` claims. Invalid, expired, wrong-issuer, wrong-audience, tampered, or non-RS256 tokens produce HTTP 401 with `{"detail":{"valid":false}}`.

## Assigned validation values
- Issuer: `https://idp.exam.local`
- Audience: `tds-8h21cceg.apps.exam.local`
- Algorithm: `RS256`

The public key in `main.py` was transcribed from the assignment screenshot. Verify that it matches the key displayed by your assignment before deploying; a single transcription error would reject all tokens.
