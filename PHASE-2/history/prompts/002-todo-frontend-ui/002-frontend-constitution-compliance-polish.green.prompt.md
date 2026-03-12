---
id: 002
title: Frontend Constitution Compliance Polish
stage: green
date: 2026-02-10
surface: agent
model: claude-opus-4-6
feature: 002-todo-frontend-ui
branch: 002-todo-frontend-ui
user: developer
command: implement plan
labels: ["accessibility", "usability", "responsiveness", "consistency", "error-handling"]
links:
  spec: specs/002-todo-frontend-ui/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - frontend/components/toast.tsx
  - frontend/components/auth-form.tsx
  - frontend/components/task-form.tsx
  - frontend/components/task-item.tsx
  - frontend/components/task-list.tsx
  - frontend/lib/api.ts
  - frontend/app/dashboard/layout.tsx
tests:
  - npx next build (TypeScript compilation, 0 errors)
---

## Prompt

Implement the following plan:

# Plan: Frontend Constitution Compliance Polish (002-todo-frontend-ui)

The frontend for the Todo Full-Stack Web Application is already built and functional. A compliance audit against the updated constitution (v1.1.0, Principles VII–XI) identified 22 specific gaps across usability, consistency, responsiveness, accuracy, and accessibility. This plan addresses those gaps with surgical edits to existing files — no rewrites, no new dependencies.

Implementation covers 6 phases: Phase 0 (toast component), Phase 1 (accessibility markup), Phase 2 (usability — inline validation, delete confirmation, character count, toast integration), Phase 3 (ApiError class for accuracy), Phase 4 (styling consistency), Phase 5 (responsive mobile-first polish with 44px touch targets).

## Response snapshot

Implemented all 6 phases across 7 files (1 new, 6 modified):

**Phase 0** — Created `toast.tsx`: lightweight fixed-position notification with aria-live, auto-dismiss after 3s, success/error variants, close button with 44px touch target.

**Phase 1 (Accessibility)** — Added `<label>` elements with `htmlFor`/`id` pairs to all form inputs. Added `role="alert" aria-live="assertive"` to error divs. Changed task-item outer `<div>` to `<article>`. Changed task-list outer `<div>` to `<section aria-label="Task list">`. Added `aria-live="polite"` to loading states. Added `aria-label` to Edit/Complete/Delete buttons including task title context. Wrapped dashboard header controls in `<nav aria-label="User actions">`. Added focus ring classes to links and sign-out button.

**Phase 2 (Usability)** — Added inline validation with `onBlur` for name, email, password fields in auth-form and title field in task-form. Added `aria-invalid` attributes. Added password hint for signup. Added character count display (gray/amber/red) for task title. Added delete confirmation with Cancel/Confirm buttons and 5s auto-reset. Integrated toast notifications for create/update/complete/delete operations.

**Phase 3 (Accuracy)** — Added `ApiError` class extending `Error` with `code` and `details` fields. Replaced `throw new Error(...)` with `throw new ApiError(...)` in `apiFetch` and `deleteTask`. Added error state to task-item for surfacing operation failures inline.

**Phase 4 (Consistency)** — Standardized button padding to `py-2` across task-item. Replaced individual `mb-3`/`mb-4` margins with `flex flex-col gap-4` in task-form.

**Phase 5 (Responsiveness)** — Added `min-h-[44px]` to all interactive elements (buttons, inputs, textareas). Changed auth-form heading to `text-xl sm:text-2xl`. Changed dashboard heading to `text-lg sm:text-xl`.

Build verified: `npx next build` compiles with 0 TypeScript errors.

## Outcome

- ✅ Impact: 22 constitution compliance gaps resolved across Principles VII–XI
- 🧪 Tests: npx next build passes (0 TypeScript errors, all pages generate)
- 📁 Files: 7 files (1 created, 6 modified)
- 🔁 Next prompts: Manual testing checklist, screen reader verification, create spec artifacts
- 🧠 Reflection: Combining phases per-file reduced double-editing and kept diffs minimal

## Evaluation notes (flywheel)

- Failure modes observed: None — all changes are additive or substitutive, no breaking changes
- Graders run and results (PASS/FAIL): TypeScript build PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run manual test checklist to verify runtime behavior
