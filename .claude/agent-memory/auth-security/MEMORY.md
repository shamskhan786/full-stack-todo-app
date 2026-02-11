# Better Auth Implementation Memory

## Project Configuration

### Better Auth Version
- Package: `better-auth@^1.0.0`
- Framework: Next.js App Router (v16.0.0)
- Database: PostgreSQL (Neon) via `pg` package

### Import Paths (v1.x)
- **Server**: `import { betterAuth } from "better-auth"`
- **JWT Plugin**: `import { jwt } from "better-auth/plugins"`
- **React Client**: `import { createAuthClient } from "better-auth/react"`
- **JWT Client Plugin**: `import { jwtClient } from "better-auth/client/plugins"`
- **Next.js Handler**: `import { toNextJsHandler } from "better-auth/next-js"`

### JWT Configuration
- **Algorithm**: EdDSA with Ed25519 curve (default, recommended)
- **JWKS Endpoint**: `/api/auth/jwks` (auto-exposed by JWT plugin)
- **Private Key Encryption**: AES256 GCM (default, enabled)
- **Storage**: Database (Neon PostgreSQL)

### Key Security Decisions
1. **EdDSA (Ed25519)** chosen over RS256:
   - Smaller keys (32 bytes vs 2048+ bits)
   - Faster signature verification
   - Equivalent security with better performance
2. **Asymmetric signing** enables backend JWT verification via JWKS
3. **Database storage** for JWKS with encryption at rest

### Environment Variables Used
- `DATABASE_URL` - PostgreSQL connection string (shared with backend)
- `BETTER_AUTH_SECRET` - Encryption key for private keys
- `BETTER_AUTH_URL` - Base URL for auth server (http://localhost:3000)
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Client-side base URL (optional, defaults to relative)

### File Locations
- Server config: `frontend/lib/auth.ts`
- Client config: `frontend/lib/auth-client.ts`
- API routes: `frontend/app/api/auth/[...all]/route.ts`

### Backend Integration
- FastAPI backend fetches JWKS from `/api/auth/jwks`
- Backend validates JWT signatures using EdDSA public keys
- No shared secret needed (asymmetric verification)

## Common Patterns

### Database Connection
```typescript
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
export const auth = betterAuth({ database: pool, ... });
```

### JWT Plugin Configuration
```typescript
jwt({
  jwks: {
    keyPairConfig: { alg: "EdDSA", crv: "Ed25519" },
    // Optional key rotation:
    // rotationInterval: 60 * 60 * 24 * 30, // 30 days
    // gracePeriod: 60 * 60 * 24 * 30,
  }
})
```

### Next.js API Route Handler
```typescript
export const { GET, POST } = toNextJsHandler(auth);
```

## Lessons Learned

1. **Better Auth v1.x uses `better-auth/plugins`** (not `better-auth/plugins/jwt`)
2. **JWT plugin auto-exposes JWKS** at `/api/auth/jwks` - no manual configuration needed
3. **EdDSA is the default and recommended** algorithm for JWT signing
4. **Database pool must be provided** - Better Auth doesn't create it automatically
5. **Environment validation is critical** - throw early if required vars are missing

## References
- [JWT Plugin Docs](https://www.better-auth.com/docs/plugins/jwt)
- [Client Docs](https://www.better-auth.com/docs/concepts/client)
- [Basic Usage](https://www.better-auth.com/docs/basic-usage)
