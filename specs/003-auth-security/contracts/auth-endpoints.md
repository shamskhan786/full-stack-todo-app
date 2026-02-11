# API Contracts: Authentication & Security

**Feature**: 003-auth-security
**Date**: 2026-02-10

## Better Auth Endpoints (Frontend, managed by library)

These endpoints are served by Next.js via the catch-all route at
`app/api/auth/[...all]/route.ts`. They are **not custom code** — Better
Auth handles request/response internally.

### POST /api/auth/sign-up/email

Create a new user account.

**Request**:
```json
{
  "name": "string",
  "email": "string",
  "password": "string (min 8 chars)"
}
```

**Success (200)**:
```json
{
  "user": { "id": "uuid", "name": "string", "email": "string" },
  "session": { "id": "uuid", "token": "string" }
}
```

**Error (422)**: Email already registered or validation failure.

### POST /api/auth/sign-in/email

Authenticate and create session.

**Request**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Success (200)**:
```json
{
  "user": { "id": "uuid", "name": "string", "email": "string" },
  "session": { "id": "uuid", "token": "string" }
}
```

**Error (401)**: Invalid credentials (generic message, does not reveal
whether email exists).

### GET /api/auth/token

Retrieve a JWT for the current session (requires valid session cookie).

**Success (200)**:
```json
{
  "token": "eyJhbGciOiJFZERTQSIs..."
}
```

Called internally by `authClient.token()` — frontend code does not call
this directly.

### POST /api/auth/sign-out

End the current session and clear cookies.

**Success (200)**: Session invalidated.

### GET /api/auth/jwks

JWKS (JSON Web Key Set) endpoint serving the public key for JWT
verification.

**Success (200)**:
```json
{
  "keys": [
    {
      "kty": "OKP",
      "crv": "Ed25519",
      "x": "base64url-encoded-public-key",
      "kid": "key-id",
      "use": "sig",
      "alg": "EdDSA"
    }
  ]
}
```

Consumed by the backend's `PyJWKClient` to verify JWT signatures.

### GET /api/auth/get-session

Return the current session and user data (requires session cookie).

**Success (200)**:
```json
{
  "user": { "id": "uuid", "name": "string", "email": "string" },
  "session": { "id": "uuid", "expiresAt": "datetime" }
}
```

**Error (401)**: No valid session.

---

## Backend Protected Endpoints (FastAPI)

All endpoints below require `Authorization: Bearer <jwt>` header. The
`verify_jwt` dependency validates the token via JWKS before any route
handler executes.

### Auth Header Contract

Every request to a protected endpoint MUST include:
```
Authorization: Bearer <jwt-token>
```

**Missing header** → `401 Unauthorized`
**Invalid/expired token** → `401 Unauthorized`
**User ID mismatch (URL vs JWT sub)** → `403 Forbidden`

### Protected Task Endpoints

All 6 task endpoints enforce both authentication (JWT) and authorization
(user_id match). Full endpoint details are in `specs/001-todo-backend-api/`.

| Method | Path | Auth | Authorization |
|--------|------|------|---------------|
| POST | `/api/{user_id}/tasks` | JWT required | URL user_id == JWT sub |
| GET | `/api/{user_id}/tasks` | JWT required | URL user_id == JWT sub |
| GET | `/api/{user_id}/tasks/{task_id}` | JWT required | URL user_id == JWT sub |
| PUT | `/api/{user_id}/tasks/{task_id}` | JWT required | URL user_id == JWT sub |
| DELETE | `/api/{user_id}/tasks/{task_id}` | JWT required | URL user_id == JWT sub |
| PATCH | `/api/{user_id}/tasks/{task_id}/complete` | JWT required | URL user_id == JWT sub |

### Error Responses

**401 Unauthorized** (missing or invalid token):
```json
{
  "detail": "Not authenticated"
}
```

**401 Unauthorized** (expired token):
```json
{
  "detail": "Token has expired"
}
```

**403 Forbidden** (user_id mismatch):
```json
{
  "detail": "User ID mismatch"
}
```

---

## Token Flow Sequence

```text
Client                    Next.js (Better Auth)         FastAPI Backend
  │                              │                            │
  │── POST /sign-in/email ──────▶│                            │
  │◀── session + cookie ─────────│                            │
  │                              │                            │
  │── GET /api/auth/token ──────▶│                            │
  │◀── { token: "eyJ..." } ─────│                            │
  │                              │                            │
  │── GET /api/{uid}/tasks ──────┼─ Authorization: Bearer ───▶│
  │                              │                            │── JWKS fetch (cached)
  │                              │◀── GET /api/auth/jwks ─────│
  │                              │── { keys: [...] } ─────────▶│
  │                              │                            │── verify signature
  │                              │                            │── check sub == uid
  │◀─────────────────────────────┼── 200 { tasks: [...] } ───│
```
