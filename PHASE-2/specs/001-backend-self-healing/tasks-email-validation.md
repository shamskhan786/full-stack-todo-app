# Tasks: Fix Email Validation Error in Signup/Signin

**Feature**: 001-backend-self-healing
**Generated**: 2026-02-12
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Overview

This task list addresses the email validation errors occurring during signup/signin operations. The issue manifests when users try to register or log in, and an error related to email validation is shown. We need to properly configure Better Auth email validation and fix the frontend validation to ensure smooth authentication flow.

## Implementation Strategy

**MVP Scope**: Fix email validation configuration and frontend validation (User Story 3)
**Delivery Order**: Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (User Story 1) → Phase 4 (User Story 2) → Phase 5 (User Story 3) → Phase 6 (Polish)
**Parallel Opportunities**: Frontend auth configuration (T001-T003) and backend email validation (T004-T006) can be developed in parallel

---

## Phase 1: Setup
Initialize project structure and core configurations for email validation fixes.

- [ ] T001 Verify current email validation configuration in `frontend/lib/auth.ts` and check if email validation settings are properly configured
- [ ] T002 [P] Check frontend environment variables in `frontend/.env.local` to ensure proper email validation settings
- [ ] T003 [P] Examine current signup form validation in `frontend/components/auth-form.tsx` to identify email validation issues

---

## Phase 2: Foundational
Implement core authentication and email validation infrastructure.

- [ ] T004 Update Better Auth configuration in `frontend/lib/auth.ts` to properly handle email validation with appropriate settings
- [ ] T005 Enhance email validation in auth client configuration in `frontend/lib/auth-client.ts` to properly handle email validation responses
- [ ] T006 Add enhanced email validation utility functions in `frontend/utils/email-validation.ts` with proper regex and validation logic
- [ ] T007 Update signup form validation in `frontend/components/auth-form.tsx` to include improved email validation and error messaging
- [ ] T008 Update signin form validation in `frontend/components/auth-form.tsx` to handle email-specific error cases properly

---

## Phase 3: User Story 1 - Backend Self-Healing Startup (Priority: P1)
The system automatically detects and fixes missing database tables, configurations, and dependencies when starting up. If Neon PostgreSQL tables are missing, they are auto-created. If authentication configuration is incomplete, it's validated and corrected.

**Goal**: Ensure email validation configuration is properly loaded on startup

**Independent Test**: Start the backend service with email validation configuration, verify that email validation rules are applied correctly and the service becomes operational without manual intervention.

- [ ] T009 [US1] Add email validation configuration to backend settings in `backend/src/config.py`
- [ ] T010 [US1] Update startup validation to check email validation configuration in `backend/src/main.py` lifespan handler
- [ ] T011 [US1] Create email validation middleware in `backend/src/middleware/email_validation.py` to validate email formats in API requests

---

## Phase 4: User Story 2 - API Endpoint Self-Healing (Priority: P2)
During API operations, if errors occur (database connection failures, missing data, authentication issues), the system attempts to recover automatically rather than failing permanently. The system validates requests and filters data by user_id to ensure proper isolation.

**Goal**: Ensure email validation errors in API requests are handled gracefully

**Independent Test**: Make API calls with invalid email formats, verify that the system handles email validation errors gracefully and maintains service availability.

- [ ] T012 [US2] Update task API endpoints to validate email-related requests in `backend/src/api/tasks.py`
- [ ] T013 [US2] Add email validation error handling in `backend/src/dependencies.py` for JWT validation
- [ ] T014 [US2] Create email validation helper functions in `backend/src/utils/email_validation.py`

---

## Phase 5: User Story 3 - Better Auth Integration (Priority: P3)
The backend seamlessly integrates with Better Auth's JWT authentication system, accepting and validating JWT tokens for all protected endpoints. The system properly handles token expiration and validation failures.

**Goal**: Ensure email validation works properly with Better Auth integration

**Independent Test**: Send API requests with JWT tokens containing emails, verify that email validation is properly handled and unauthorized access is prevented.

- [ ] T015 [US3] Update JWT validation to include email validation in `backend/src/dependencies.py`
- [ ] T016 [US3] Add email validation in health check endpoint in `backend/src/api/health.py`
- [ ] T017 [US3] Test email validation with Better Auth integration in `backend/tests/test_auth_email_validation.py`

---

## Phase 6: Polish & Cross-Cutting Concerns
Final touches and cross-cutting concerns for email validation.

- [ ] T018 Add comprehensive email validation tests in `frontend/__tests__/auth-form.test.tsx`
- [ ] T019 Update documentation for email validation configuration in `specs/001-backend-self-healing/quickstart.md`
- [ ] T020 Add error logging for email validation failures in both frontend and backend
- [ ] T021 Test the complete signup/signin flow to verify email validation errors are fixed

---

## Dependencies

**User Story Completion Order**: US1 → US2 → US3 (US1 must be complete before US2, US2 before US3)

## Parallel Execution Examples

**Per Story 1**: T009, T010, T011 can run in parallel since they modify different files
**Per Story 2**: T012, T013, T014 can run in parallel since they modify different files
**Per Story 3**: T015, T016, T017 can run in parallel since they modify different files
