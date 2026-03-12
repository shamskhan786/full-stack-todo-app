# Implementation Plan: Todo Full-Stack Web Application – Frontend & Basic Features

**Branch**: `002-todo-frontend-ui` | **Date**: 2026-02-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-todo-frontend-ui/spec.md`

## Summary

Build a responsive, accessible, and user-friendly frontend for the
Todo application using Next.js 16+ App Router. The backend API (6
RESTful endpoints) and authentication (Better Auth with JWT) are
already implemented and tested. This feature focuses on polishing the
existing frontend to comply with constitution principles VII–XI:
Usability, Consistency, Responsiveness, Frontend–Backend Accuracy,
and Accessibility.

## Technical Context

**Language/Version**: TypeScript / Node.js 20+ / Next.js 16+
**Primary Dependencies**: React 19, Better Auth, Tailwind CSS 3.4
**Storage**: N/A (frontend communicates via REST API to FastAPI backend)
**Testing**: Manual browser testing (375px, 768px, 1920px viewports)
**Target Platform**: Web (desktop + mobile responsive)
**Project Type**: Web application (frontend portion)
**Performance Goals**: All task operations update UI within 1 second
**Constraints**: Mobile-first responsive, no new npm dependencies
**Scale/Scope**: 5 pages, 4 components, 1 API client, 1 new component

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| VII. Usability | Inline validation, delete confirmation, loading/error/empty states | PASS (with fixes planned) |
| VIII. Consistency | Uniform button sizing, form spacing, success feedback | PASS (with fixes planned) |
| IX. Responsiveness | 44px touch targets, responsive typography, mobile-first | PASS (with fixes planned) |
| X. Accuracy | Centralized API client, error surfacing, no silent failures | PASS (with fixes planned) |
| XI. Accessibility | Labels, aria attrs, semantic HTML, focus rings, no color-only | PASS (with fixes planned) |
| I–VI. Backend | Already verified in 001-todo-backend-api | PASS |

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-frontend-ui/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Frontend technology decisions
├── data-model.md        # References backend data model
├── quickstart.md        # Frontend setup instructions
├── contracts/           # References backend OpenAPI contract
└── tasks.md             # Task breakdown (via /sp.tasks)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── (auth)/
│   │   ├── signin/page.tsx      # Sign-in page
│   │   └── signup/page.tsx      # Sign-up page
│   ├── api/auth/[...all]/
│   │   └── route.ts             # Better Auth API handler
│   ├── dashboard/
│   │   ├── layout.tsx           # Protected layout (MODIFY)
│   │   └── page.tsx             # Dashboard page
│   ├── globals.css
│   ├── layout.tsx               # Root layout
│   └── page.tsx                 # Home redirect
├── components/
│   ├── auth-form.tsx            # Auth form (MODIFY)
│   ├── task-form.tsx            # Task create/edit form (MODIFY)
│   ├── task-item.tsx            # Task item display (MODIFY)
│   ├── task-list.tsx            # Task list with CRUD (MODIFY)
│   └── toast.tsx                # Toast notifications (NEW)
├── lib/
│   ├── api.ts                   # API client (MODIFY)
│   ├── auth.ts                  # Better Auth server config
│   └── auth-client.ts           # Better Auth client config
└── package.json
```

**Structure Decision**: Web application — frontend-only changes.
Backend structure unchanged from 001-todo-backend-api.

## Key Technical Decisions

### D1: No New Dependencies
All compliance fixes use native browser APIs, React state, and
Tailwind CSS utility classes. No animation, toast, or accessibility
libraries added. Rationale: minimize bundle size and dependency
surface for a small application.

### D2: Inline Delete Confirmation (not Modal)
Delete confirmation uses inline "Cancel | Confirm" buttons replacing
the Delete button, not a modal dialog. Rationale: simpler
implementation, no portal needed, works well on mobile, and avoids
focus-trap complexity.

### D3: Field-Level ApiError Class
A custom `ApiError` class extending `Error` carries `code` and
`details` fields from the backend's ErrorResponse. Non-breaking:
existing catch blocks still work since `ApiError extends Error`.

### D4: Toast Component (Lightweight)
A single-file toast component using fixed positioning and auto-dismiss.
No toast queue, no stacking — one toast at a time is sufficient for
this application's interaction patterns.

## Implementation Phases

### Phase 0: Foundation — Toast Component (1 new file)
- Create `frontend/components/toast.tsx`
- Fixed-position, auto-dismiss, aria-live for screen readers

### Phase 1: Accessibility (Principle XI)
- Add `<label>` elements to all form inputs
- Add `aria-label` to all action buttons
- Add `aria-live` regions for loading/error states
- Use semantic elements (`<article>`, `<section>`, `<nav>`)
- Add visible focus rings to links and buttons
- Add password requirement hint with `aria-describedby`

### Phase 2: Usability (Principle VII)
- Delete confirmation on task-item.tsx
- Inline validation (onBlur) on auth-form.tsx and task-form.tsx
- Character count display on task title field
- Toast notifications for success/error on all CRUD operations

### Phase 3: Accuracy (Principle X)
- `ApiError` class in api.ts for field-level error propagation
- Error state and display on task-item.tsx

### Phase 4: Consistency (Principle VIII)
- Standardize button padding (`py-2` everywhere)
- Standardize form spacing (`gap-4` everywhere)

### Phase 5: Responsiveness (Principle IX)
- `min-h-[44px]` on all interactive elements for mobile touch targets
- Responsive typography (`text-xl sm:text-2xl`)

## Complexity Tracking

No constitution violations. All changes are compliance fixes within
the existing architecture.

## Risks

1. **Layout shift from inline delete confirmation**: Mitigated by
   using consistent button widths.
2. **Toast z-index conflicts**: Mitigated by z-50 (highest Tailwind
   tier) and no other fixed elements in the app.
3. **ApiError serialization across Next.js boundary**: Not a risk —
   ApiError is only used in client-side api.ts.
