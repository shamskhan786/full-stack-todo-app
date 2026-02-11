# Research: Authentication & Security Technology Decisions

**Feature**: 003-auth-security
**Date**: 2026-02-10

## Decision 1: Frontend Authentication Library

**Decision**: Better Auth with JWT plugin (EdDSA/Ed25519)

**Rationale**: Better Auth is the mandated auth library per the
constitution. The JWT plugin enables stateless token issuance that
the backend can verify without shared secrets. EdDSA (Ed25519) was
chosen for its speed, small key size, and modern security profile.

**Alternatives considered**:
- NextAuth.js — popular but does not natively support JWT issuance
  with asymmetric signing for cross-service verification
- Custom JWT implementation — unnecessary complexity when Better Auth
  provides a well-tested JWT plugin
- Session-based auth — violates constitution Principle XV
  (Statelessness)

## Decision 2: Backend Token Verification Method

**Decision**: JWKS endpoint verification using PyJWT + PyJWKClient

**Rationale**: The backend fetches the public key from Better Auth's
JWKS endpoint (`/api/auth/jwks`) to verify JWT signatures. This is
superior to shared-secret verification because:
1. The signing private key never leaves the frontend server
2. Key rotation is automatic (JWKS serves current keys)
3. No `BETTER_AUTH_SECRET` needed in backend config

**Alternatives considered**:
- Shared secret (HMAC) — requires distributing the secret to both
  services; less secure than asymmetric keys
- Manual public key configuration — brittle; breaks on key rotation
- Auth service proxy — unnecessary middleware; adds latency

## Decision 3: User Identity Claim

**Decision**: JWT `sub` (subject) claim containing user UUID

**Rationale**: The `sub` claim is the RFC 7519 standard for
identifying the principal that is the subject of the JWT. Better Auth
sets this to the user's database ID (UUID). Using a standard claim
ensures interoperability and avoids custom claim parsing.

**Alternatives considered**:
- Custom `user_id` claim — non-standard, requires claim mapping
- `email` claim — not a stable identifier (emails can change)
- Nested claim object — over-engineered for a single identity value

## Decision 4: Authorization Pattern

**Decision**: Per-route `_verify_user_id()` helper comparing URL
parameter against JWT `sub` claim

**Rationale**: Every route that includes `{user_id}` in the path
calls `_verify_user_id()` to ensure the URL parameter matches the
authenticated user. This is explicit, auditable, and fails closed
(403 on mismatch).

**Alternatives considered**:
- Middleware-based extraction — harder to reason about; implicit
- Decorator pattern — adds indirection without benefit for 6 routes
- Removing user_id from URL — breaks RESTful resource hierarchy

## Decision 5: Frontend Token Management

**Decision**: Better Auth client manages token lifecycle;
`authClient.token()` retrieves JWT for API calls

**Rationale**: Better Auth's `jwtClient` plugin provides
`authClient.token()` which returns the current JWT. The centralized
`api.ts` calls this before every request and attaches the token as
`Authorization: Bearer <token>`. This keeps token management in one
place and avoids scattered auth logic.

**Alternatives considered**:
- Manual localStorage management — insecure (XSS exposure) and
  requires custom refresh logic
- HTTP-only cookie — incompatible with cross-origin API calls to
  separate backend server
- Interceptor-based attachment — unnecessary when centralized
  `apiFetch()` already handles it

## Decision 6: Test Authentication Strategy

**Decision**: FastAPI dependency overrides for `verify_jwt` in tests

**Rationale**: Tests override `verify_jwt` to return a fixed payload
(`{"sub": TEST_USER_ID}`), bypassing real JWT verification. This
allows testing business logic without running Better Auth. Three
fixtures cover: authenticated user, other user (isolation tests),
and unauthenticated (401 tests).

**Alternatives considered**:
- Generating real JWTs in tests — requires running Better Auth
  server; slow and fragile
- Mocking HTTP requests — over-mocking; tests don't exercise
  FastAPI dependency injection
- Test-specific auth middleware — duplicates production code
