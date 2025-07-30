# Authentication Guide

This project supports authentication via username/password, GitHub OAuth, and Google OAuth. All authenticated API endpoints require a valid JWT Bearer token.

## 1. Username/Password Login

1. Register a user (with OTP verification):
   - `POST /api/v1/users/register` with JSON body `{ "email": ..., "name": ..., "password": ... }`
   - `POST /api/v1/users/verify-otp` with JSON body `{ "email": ..., "otp_code": ... }`
2. Login:
   - `POST /api/v1/users/login` with form data `username` and `password`.
   - The response will include `{ "access_token": "<JWT>", "token_type": "bearer" }`.


## 2. GitHub OAuth Login

1. Go to `/api/v1/auth/github/login` in your browser.
2. Authorize the app on GitHub.
3. You will be redirected back and receive a JSON response with `{ "access_token": "<JWT>", "token_type": "bearer" }`.

## 3. Google OAuth Login

1. Go to `/api/v1/auth/google/login` in your browser.
2. Authorize the app with your Google account.
3. You will be redirected back and receive a JSON response with `{ "access_token": "<JWT>", "token_type": "bearer" }`.

## 4. Using the Token in Swagger UI

- Open `/docs` (Swagger UI).
- Click the "Authorize" button.
- **Paste only the JWT token** (do NOT include the `Bearer ` prefix).
- Click "Authorize".
- You can now access all authenticated endpoints.

## 5. Using the Token in API Clients (e.g., Postman)

- Set the `Authorization` header:
  ```
  Authorization: <your_token>
  ```

## 6. Notes

- The same JWT token format is used for both login methods.
- If you get a credentials error, ensure you are pasting only the token (not `Bearer <token>`) in Swagger UI.
- For GitHub and Google login, the user is auto-registered on first login if not already present.

---

For more details, see the code in `app/services/user.py` and `app/api/routes/auth.py`.
