# Tasks: Todo Full-Stack Web Application – Authentication & Security

**Input**: Design documents from `/specs/003-auth-security/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Not explicitly requested. Existing backend tests (22/22 passing) already cover auth and isolation.

**Organization**: Tasks are grouped by user story. Since auth is **already implemented** (14/15 FRs done), tasks focus on verifying existing implementation and fixing the one identified gap (FR-011).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Verification Setup

**Purpose**: Confirm existing implementation matches spec before making changes

- [x] T001 Verify backend auth dependencies installed: `PyJWT[crypto]`, `cryptography` in `backend/requirements.txt`
- [x] T002 [P] Verify frontend auth dependencies installed: `better-auth`, `pg` in `frontend/package.json`
- [x] T003 [P] Verify environment configuration: `JWKS_URL` in `backend/src/config.py`, `BETTER_AUTH_SECRET` and `NEXT_PUBLIC_BETTER_AUTH_URL` in frontend env schema
- [x] T004 Run backend test suite: `cd backend && python -m pytest tests/ -v` — all 22 tests must pass

**Checkpoint**: Existing implementation confirmed healthy; safe to proceed with gap fix

---

## Phase 2: Foundational (No Blocking Prerequisites)

**Purpose**: No new foundational work needed — auth infrastructure is already in place

- [x] T005 Verify `verify_jwt` dependency accepts EdDSA/ES256/RS256 algorithms in `backend/src/dependencies.py`
- [x] T006 [P] Verify JWKS client caching (singleton `_jwks_client`) in `backend/src/dependencies.py`
- [x] T007 [P] Verify CORS allows `Authorization` header in `backend/src/main.py`
- [x] T008 [P] Verify Better Auth server config with JWT plugin (EdDSA/Ed25519) in `frontend/lib/auth.ts`
- [x] T009 [P] Verify Better Auth client config with `jwtClient` plugin in `frontend/lib/auth-client.ts`

**Checkpoint**: Foundation verified — all auth infrastructure operational

---

## Phase 3: User Story 1 — User Sign-Up (Priority: P1)

**Goal**: New users can create accounts with name, email, and password

**Independent Test**: Visit `/signup`, fill form, submit, verify account created and redirected to sign-in

### Verification for User Story 1

- [x] T010 [US1] Verify Better Auth `emailAndPassword.enabled: true` in `frontend/lib/auth.ts`
- [x] T011 [P] [US1] Verify sign-up form collects name, email, password with inline validation in `frontend/components/auth-form.tsx`
- [x] T012 [P] [US1] Verify sign-up page renders auth form in sign-up mode at `frontend/app/(auth)/signup/page.tsx`
- [x] T013 [US1] Verify password minimum length validation (8 chars) in `frontend/components/auth-form.tsx`
- [x] T014 [US1] Verify duplicate email error handling in `frontend/components/auth-form.tsx`

**Checkpoint**: US1 verified — sign-up flow works end-to-end

---

## Phase 4: User Story 2 — User Sign-In and Token Issuance (Priority: P1)

**Goal**: Registered users can sign in and receive a JWT containing their user ID

**Independent Test**: Sign in with valid credentials, verify JWT issued with `sub` claim, verify redirect to dashboard

### Verification for User Story 2

- [x] T015 [US2] Verify sign-in form in `frontend/components/auth-form.tsx` calls `signIn.email()`
- [x] T016 [P] [US2] Verify sign-in page renders auth form in sign-in mode at `frontend/app/(auth)/signin/page.tsx`
- [x] T017 [US2] Verify `authClient.token()` returns JWT with `sub` claim via `frontend/lib/auth-client.ts`
- [x] T018 [US2] Verify generic error message on invalid credentials (does not reveal email existence) in `frontend/components/auth-form.tsx`

**Checkpoint**: US2 verified — sign-in and token issuance work end-to-end

---

## Phase 5: User Story 3 — Authenticated API Access (Priority: P1)

**Goal**: Every API request includes the JWT; backend verifies before processing

**Independent Test**: Make API call with valid token (succeeds), without token (401), with expired token (401 + redirect)

### Verification for User Story 3

- [x] T019 [US3] Verify `apiFetch()` attaches `Authorization: Bearer <token>` header in `frontend/lib/api.ts`
- [x] T020 [P] [US3] Verify `verify_jwt` returns 401 for missing token via `HTTPBearer` in `backend/src/dependencies.py`
- [x] T021 [P] [US3] Verify `verify_jwt` returns 401 for expired token (`jwt.ExpiredSignatureError`) in `backend/src/dependencies.py`
- [x] T022 [P] [US3] Verify `verify_jwt` returns 401 for tampered token (`jwt.InvalidTokenError`) in `backend/src/dependencies.py`
- [x] T023 [US3] Verify backend tests cover no-auth and wrong-token scenarios in `backend/tests/test_tasks.py`

### Implementation for User Story 3 (FR-011 Gap Fix)

- [x] T024 [US3] Add 401 response detection in `apiFetch()` to redirect to `/signin` when backend rejects token in `frontend/lib/api.ts`
- [x] T025 [US3] Add 401 response detection in `deleteTask()` to redirect to `/signin` in `frontend/lib/api.ts`
- [x] T026 [US3] Verify Next.js build passes after FR-011 fix: `cd frontend && npx next build`

**Checkpoint**: US3 verified and fixed — all API calls authenticated, 401 triggers redirect

---

## Phase 6: User Story 4 — User-Scoped Data Isolation (Priority: P1)

**Goal**: Users can only access their own tasks; cross-user access returns 403

**Independent Test**: Create tasks as User A, attempt access as User B via API, verify 403

### Verification for User Story 4

- [x] T027 [US4] Verify `_verify_user_id()` compares URL `user_id` against JWT `sub` in `backend/src/api/tasks.py`
- [x] T028 [P] [US4] Verify all 6 route handlers call `_verify_user_id()` before business logic in `backend/src/api/tasks.py`
- [x] T029 [P] [US4] Verify all queries scope by `user_id` (`WHERE Task.user_id == user_id`) in `backend/src/api/tasks.py`
- [x] T030 [US4] Verify backend tests cover cross-user isolation (`test_list_tasks_isolation`, `test_create_task_wrong_user`) in `backend/tests/test_tasks.py`

**Checkpoint**: US4 verified — complete user isolation enforced

---

## Phase 7: User Story 5 — Sign-Out (Priority: P2)

**Goal**: Users can sign out, clearing client-side auth state and redirecting to sign-in

**Independent Test**: Sign in, access dashboard, sign out, verify redirect, verify dashboard inaccessible

### Verification for User Story 5

- [x] T031 [US5] Verify sign-out button calls `signOut()` and redirects to `/signin` in `frontend/app/dashboard/layout.tsx`
- [x] T032 [US5] Verify `signOut` is exported from `frontend/lib/auth-client.ts`

**Checkpoint**: US5 verified — sign-out clears auth state

---

## Phase 8: User Story 6 — Protected Route Enforcement (Priority: P2)

**Goal**: Unauthenticated users are redirected to sign-in when accessing protected pages

**Independent Test**: Navigate to `/dashboard` without session, verify redirect to `/signin` with no content flash

### Verification for User Story 6

- [x] T033 [US6] Verify `useSession()` check in `frontend/app/dashboard/layout.tsx` redirects unauthenticated users
- [x] T034 [US6] Verify loading state prevents content flash before session check completes in `frontend/app/dashboard/layout.tsx`

**Checkpoint**: US6 verified — protected routes enforce authentication

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final validation across all user stories

- [x] T035 Run full backend test suite: `cd backend && python -m pytest tests/ -v` — all 22 tests must pass
- [x] T036 [P] Run frontend build verification: `cd frontend && npx next build` — zero errors
- [x] T037 Validate quickstart checklist from `specs/003-auth-security/quickstart.md` (manual)
- [x] T038 Verify constitution compliance: Principles XII–XVI from `.specify/memory/constitution.md` (manual)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Verification Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 passing
- **Phases 3–8 (User Stories)**: All depend on Phase 2 verification passing
  - US1 (Phase 3): Independent
  - US2 (Phase 4): Independent
  - US3 (Phase 5): Independent — **contains the only code change** (T024–T026)
  - US4 (Phase 6): Independent
  - US5 (Phase 7): Independent
  - US6 (Phase 8): Independent
- **Phase 9 (Polish)**: Depends on all user story phases complete

### User Story Dependencies

- **US1 (Sign-Up)**: No dependencies on other stories
- **US2 (Sign-In)**: Independent (requires US1 for end-to-end but independently verifiable)
- **US3 (API Access)**: Independent — **only story with code changes** (FR-011 fix)
- **US4 (Data Isolation)**: Independent
- **US5 (Sign-Out)**: Independent
- **US6 (Protected Routes)**: Independent

### Within User Story 3 (the only implementation story)

1. Verify existing behavior (T019–T023) — confirms current state
2. Implement FR-011 fix (T024–T025) — add 401 redirect
3. Build verification (T026) — confirms no regressions

### Parallel Opportunities

- Phase 1: T001, T002, T003 can run in parallel
- Phase 2: T005–T009 all parallelizable (verification of different files)
- User Stories: All 6 stories can be verified in parallel (only US3 has code changes)
- Phase 9: T035 and T036 can run in parallel

---

## Parallel Example: Phase 2 Verification

```bash
# All verification tasks touch different files — run in parallel:
Task: "Verify verify_jwt algorithms in backend/src/dependencies.py"
Task: "Verify CORS Authorization header in backend/src/main.py"
Task: "Verify Better Auth server config in frontend/lib/auth.ts"
Task: "Verify Better Auth client config in frontend/lib/auth-client.ts"
```

## Parallel Example: User Story 3 (FR-011 Fix)

```bash
# Verify existing auth behavior in parallel:
Task: "Verify apiFetch attaches Bearer token in frontend/lib/api.ts"
Task: "Verify verify_jwt returns 401 for missing token in backend/src/dependencies.py"
Task: "Verify verify_jwt returns 401 for expired token in backend/src/dependencies.py"

# Then implement sequentially:
Task: "Add 401 detection in apiFetch() in frontend/lib/api.ts"
Task: "Add 401 detection in deleteTask() in frontend/lib/api.ts"
Task: "Build verification: npx next build"
```

---

## Implementation Strategy

### MVP First (Verification Only)

1. Complete Phase 1: Run existing tests to confirm health
2. Complete Phase 2: Verify all foundational auth components
3. **STOP and REPORT**: If all verification passes, auth is confirmed working

### Gap Fix (FR-011)

1. After verification passes, proceed to Phase 5 (US3)
2. Implement T024–T025: Add 401 redirect in `api.ts`
3. Run T026: Build verification
4. **STOP and VALIDATE**: Test 401 redirect manually

### Full Validation

1. Complete all remaining verification phases (US1–US6)
2. Run Phase 9 polish tasks
3. All 38 tasks complete

---

## Notes

- **34 of 38 tasks are verification-only** (no code changes)
- **4 tasks require code changes**: T024, T025, T026 (FR-011 fix), T035 (re-run tests)
- The FR-011 fix is contained entirely within `frontend/lib/api.ts`
- Existing backend tests (22/22) are not modified — they already cover auth
- [P] tasks = different files, no dependencies
- Stop at any checkpoint to validate independently
