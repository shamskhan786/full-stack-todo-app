# Tasks: Todo Full-Stack Web Application – Frontend & Basic Features

**Input**: Design documents from `/specs/002-todo-frontend-ui/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Not explicitly requested — no test tasks included. Verification is via manual browser testing and `npx next build` compilation check.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/` at repository root
- **Components**: `frontend/components/`
- **Pages**: `frontend/app/`
- **Libraries**: `frontend/lib/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create shared components and enhance the API client that all user stories depend on

- [x] T001 Create toast notification component in `frontend/components/toast.tsx` — fixed-position, auto-dismiss after 3s, `aria-live="polite"`, success/error variants, close button with `aria-label="Dismiss notification"` and 44px touch target
- [x] T002 Add `ApiError` class extending `Error` with `code` and `details` fields in `frontend/lib/api.ts` — replace `throw new Error(...)` with `throw new ApiError(...)` in `apiFetch` and `deleteTask` functions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Accessibility and semantic HTML infrastructure that MUST be complete before user story polish can be applied

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 [P] Add semantic `<section aria-label="Task list">` wrapper, `role="status" aria-live="polite"` on loading div, and `role="alert" aria-live="assertive"` on error div in `frontend/components/task-list.tsx`
- [x] T004 [P] Wrap email + sign-out in `<nav aria-label="User actions">`, add `aria-label="Sign out"` and focus ring classes (`focus:outline-none focus:ring-2 focus:ring-red-500 rounded`) to sign-out button in `frontend/app/dashboard/layout.tsx`
- [x] T005 [P] Change outer `<div>` to `<article>` element in `frontend/components/task-item.tsx` for semantic task representation

**Checkpoint**: Foundation ready — semantic HTML and ARIA infrastructure in place for all user story phases

---

## Phase 3: User Story 1 – User Authentication (Priority: P1) 🎯 MVP

**Goal**: Polish the sign-up/sign-in forms with labels, inline validation, password hints, and accessible error handling so users can securely authenticate with full client-side validation and screen reader support.

**Independent Test**: Visit sign-up page → verify labels visible, tab to each field → verify focus rings, blur email with invalid format → verify inline error appears, blur password with < 8 chars → verify error, submit empty form → verify inline errors fire before server submission, sign in with valid credentials → verify redirect to dashboard.

### Implementation for User Story 1

- [x] T006 [P] [US1] Add `<label htmlFor="auth-name">Name</label>` with `id="auth-name"` on the name input in `frontend/components/auth-form.tsx` (signup mode only)
- [x] T007 [P] [US1] Add `<label htmlFor="auth-email">Email</label>` with `id="auth-email"` on the email input in `frontend/components/auth-form.tsx`
- [x] T008 [P] [US1] Add `<label htmlFor="auth-password">Password</label>` with `id="auth-password"` on the password input in `frontend/components/auth-form.tsx`
- [x] T009 [US1] Add password hint `<p id="password-hint">Minimum 8 characters</p>` with `aria-describedby="password-hint"` on password input (signup mode only) in `frontend/components/auth-form.tsx`
- [x] T010 [US1] Add `nameError`, `emailError`, `passwordError` state variables and `onBlur` validation functions — name required (signup), email format regex, password min 8 chars — in `frontend/components/auth-form.tsx`
- [x] T011 [US1] Display field-level error `<p role="alert">` after each input with `aria-invalid` attribute when field has error in `frontend/components/auth-form.tsx`
- [x] T012 [US1] Add `role="alert" aria-live="assertive"` to the existing server error div in `frontend/components/auth-form.tsx`
- [x] T013 [US1] Add focus ring classes (`focus:outline-none focus:ring-2 focus:ring-blue-500 rounded`) to Sign Up and Sign In navigation links in `frontend/components/auth-form.tsx`
- [x] T014 [US1] Add `min-h-[44px]` to all inputs and submit button for 44px touch target compliance in `frontend/components/auth-form.tsx`
- [x] T015 [US1] Change heading from `text-2xl` to `text-xl sm:text-2xl` for responsive typography in `frontend/components/auth-form.tsx`

**Checkpoint**: User Story 1 complete — sign-up and sign-in forms have labels, inline validation, password hints, ARIA attributes, focus rings, responsive type, and 44px touch targets

---

## Phase 4: User Story 2 – View and Create Tasks (Priority: P2)

**Goal**: Polish the task creation form with labels, character count, inline validation, and toast success feedback so users get immediate, accessible feedback when creating tasks.

**Independent Test**: Sign in → click "+ New Task" → verify "Title" and "Description (optional)" labels visible, type title → verify character count shows `{n}/500`, approach 450 chars → verify amber color, blur empty title → verify inline error, submit valid task → verify toast "Task created successfully" appears, verify task appears in list.

### Implementation for User Story 2

- [x] T016 [P] [US2] Add `<label htmlFor="task-title">Title</label>` with `id="task-title"` on the title input in `frontend/components/task-form.tsx`
- [x] T017 [P] [US2] Add `<label htmlFor="task-desc">Description (optional)</label>` with `id="task-desc"` on the textarea in `frontend/components/task-form.tsx`
- [x] T018 [US2] Add `titleError` state and `onBlur` validation function (title required, max 500 chars) in `frontend/components/task-form.tsx`
- [x] T019 [US2] Display field-level error `<p id="title-error" role="alert">` and `aria-invalid` / `aria-describedby` on input in `frontend/components/task-form.tsx`
- [x] T020 [US2] Add character count display `<span>{title.length}/500</span>` below title input — gray default, amber at 450+, red at 500+ — in `frontend/components/task-form.tsx`
- [x] T021 [US2] Add `role="alert" aria-live="assertive"` to the existing form error div in `frontend/components/task-form.tsx`
- [x] T022 [US2] Replace `mb-3`/`mb-4` individual margins with `flex flex-col gap-4` on the form element for consistent spacing in `frontend/components/task-form.tsx`
- [x] T023 [US2] Add `min-h-[44px]` to title input, textarea, Cancel button, and Submit button for 44px touch targets in `frontend/components/task-form.tsx`
- [x] T024 [US2] Add `toast` state (`{message, type} | null`) and import `Toast` component in `frontend/components/task-list.tsx`
- [x] T025 [US2] Trigger success toast `"Task created successfully"` after `handleCreate` completes in `frontend/components/task-list.tsx`
- [x] T026 [US2] Add `min-h-[44px]` to "+ New Task" and "Try again" buttons in `frontend/components/task-list.tsx`

**Checkpoint**: User Story 2 complete — task creation form has labels, inline validation, character count, consistent spacing, toast feedback, and 44px touch targets

---

## Phase 5: User Story 3 – Edit and Delete Tasks (Priority: P3)

**Goal**: Add delete confirmation, inline error surfacing, and toast feedback for edit/delete operations so users are protected from accidental deletions and informed of failures.

**Independent Test**: Create a task → click Edit → verify form pre-filled with title/description, update title → submit → verify toast "Task updated successfully", click Delete → verify "Cancel" and "Confirm" buttons appear (not immediate deletion), wait 5s → verify confirmation auto-resets, click Delete → Confirm → verify toast "Task deleted" and task removed from list.

### Implementation for User Story 3

- [x] T027 [US3] Add `confirmDelete` state (boolean) to `frontend/components/task-item.tsx`
- [x] T028 [US3] Replace single Delete button with conditional render: default shows "Delete", on click switches to "Cancel | Confirm" inline buttons in `frontend/components/task-item.tsx`
- [x] T029 [US3] Add `useEffect` to auto-reset `confirmDelete` to false after 5 seconds in `frontend/components/task-item.tsx`
- [x] T030 [US3] Add `error` state to `frontend/components/task-item.tsx` — show error message below action buttons when complete/delete fails, clear on next action
- [x] T031 [US3] Add `aria-label` attributes to Edit (`Edit task: {title}`), Complete (`Mark complete: {title}`), Delete (`Delete task: {title}`), and Confirm (`Confirm delete: {title}`) buttons in `frontend/components/task-item.tsx`
- [x] T032 [US3] Trigger success toast `"Task updated successfully"` after `handleUpdate` and `"Task deleted"` after `handleDelete` in `frontend/components/task-list.tsx`
- [x] T033 [US3] Trigger error toast on failed complete/delete operations in `handleComplete` and `handleDelete` in `frontend/components/task-list.tsx`
- [x] T034 [US3] Standardize button padding from `py-1.5` to `py-2` across all buttons in `frontend/components/task-item.tsx`
- [x] T035 [US3] Add `min-h-[44px]` to all buttons (Edit, Complete, Delete, Cancel, Confirm) in `frontend/components/task-item.tsx`

**Checkpoint**: User Story 3 complete — edit triggers toast, delete has confirmation prompt with 5s auto-reset, errors surface inline, all buttons have ARIA labels and 44px touch targets

---

## Phase 6: User Story 4 – Mark Tasks as Complete (Priority: P4)

**Goal**: Ensure completed tasks are visually distinguishable using both styling AND a text/icon indicator (not color alone), with accessible completion feedback.

**Independent Test**: Create a task → click Complete → verify checkmark (✓) appears alongside "Completed" text → verify toast "Task completed" → verify completed task has distinct styling (strikethrough, green border) → refresh page → verify completion state persists.

### Implementation for User Story 4

- [x] T036 [US4] Add checkmark prefix `✓` to the "Completed" text span (currently shows only `Completed {date}`) in `frontend/components/task-item.tsx` — ensures completion is indicated by text/icon, not color alone
- [x] T037 [US4] Trigger success toast `"Task completed"` after `handleComplete` in `frontend/components/task-list.tsx`

**Checkpoint**: User Story 4 complete — completed tasks show ✓ icon + "Completed" text + green styling, toast confirms action

---

## Phase 7: User Story 5 – Responsive Layout (Priority: P5)

**Goal**: Ensure the dashboard layout is fully responsive with proper touch targets, readable typography, and no horizontal scrolling from 375px to 1920px.

**Independent Test**: Set browser to 375px width → navigate through sign-in, dashboard, create/edit/delete task → verify no horizontal scroll, all buttons ≥ 44px height, text readable. Repeat at 768px and 1920px.

### Implementation for User Story 5

- [x] T038 [US5] Change dashboard heading from `text-xl` to `text-lg sm:text-xl` for responsive typography in `frontend/app/dashboard/layout.tsx`
- [x] T039 [US5] Add `min-h-[44px]` and `px-2` to sign-out button for 44px touch target in `frontend/app/dashboard/layout.tsx`

**Checkpoint**: User Story 5 complete — all viewports (375px, 768px, 1920px) display correctly with no horizontal scroll, adequate touch targets, and responsive typography

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation

- [x] T040 Run `npx next build` in `frontend/` to verify zero TypeScript/compilation errors
- [ ] T041 Manual verification: tab through all interactive elements on sign-up, sign-in, and dashboard pages → verify visible focus rings on every focusable element
- [ ] T042 Manual verification: resize browser to 375px → verify no horizontal scrollbar, all buttons ≥ 44px height, forms usable
- [ ] T043 Manual verification: complete full lifecycle (sign up → sign in → create → edit → complete → delete → sign out) → verify toasts appear for each CRUD action
- [ ] T044 Manual verification: test delete confirmation flow — click Delete → see Cancel/Confirm → click Cancel → verify deletion cancelled; click Delete → Confirm → verify task removed
- [ ] T045 Manual verification: test inline validation — blur empty email → see error, blur short password → see error, blur empty task title → see error

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 (toast component needed for Phase 2 semantic markup, ApiError for Phase 2 error handling)
- **User Stories (Phase 3–7)**: All depend on Phase 2 completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3 → P4 → P5)
  - Or in parallel where files don't overlap
- **Polish (Phase 8)**: Depends on all user story phases being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 — modifies `auth-form.tsx` only
- **User Story 2 (P2)**: Can start after Phase 2 — modifies `task-form.tsx` and `task-list.tsx`
- **User Story 3 (P3)**: Can start after Phase 2 — modifies `task-item.tsx` and `task-list.tsx`; if running parallel with US2, coordinate `task-list.tsx` changes
- **User Story 4 (P4)**: Can start after Phase 2 — modifies `task-item.tsx` and `task-list.tsx`; if running parallel with US3, coordinate shared files
- **User Story 5 (P5)**: Can start after Phase 2 — modifies `dashboard/layout.tsx` only; fully parallel with US1–US4

### Within Each User Story

- Labels and semantic markup first (additive, no conflicts)
- Validation state and behavior second (depends on labels for `htmlFor`/`id` pairing)
- Styling normalization and touch targets last (additive class changes on final state)

### Parallel Opportunities

- **Phase 1**: T001 and T002 are independent (different files) — can run in parallel
- **Phase 2**: T003, T004, T005 are independent (different files) — can run in parallel
- **US1**: T006, T007, T008 are independent label additions — can run in parallel
- **US2**: T016, T017 are independent label additions — can run in parallel
- **US1 and US5**: Modify different files — can run fully in parallel
- **US1 and US2**: Modify different files — can run fully in parallel

---

## Parallel Example: Phase 1 (Setup)

```bash
# Launch both setup tasks in parallel (different files):
Task: "Create toast component in frontend/components/toast.tsx"
Task: "Add ApiError class in frontend/lib/api.ts"
```

## Parallel Example: User Story 1

```bash
# Launch all label tasks in parallel (same file but different sections, no overlap):
Task: "Add name label in frontend/components/auth-form.tsx"
Task: "Add email label in frontend/components/auth-form.tsx"
Task: "Add password label in frontend/components/auth-form.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (toast + ApiError)
2. Complete Phase 2: Foundational (semantic HTML + ARIA infrastructure)
3. Complete Phase 3: User Story 1 (auth form polish)
4. **STOP and VALIDATE**: Test sign-up/sign-in flow independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Infrastructure ready
2. Add User Story 1 → Test auth forms → Deploy (MVP!)
3. Add User Story 2 → Test task creation → Deploy
4. Add User Story 3 → Test edit/delete → Deploy
5. Add User Story 4 → Test completion marking → Deploy
6. Add User Story 5 → Test responsive layout → Deploy
7. Each story adds value without breaking previous stories

---

## Summary

- **Total tasks**: 45
- **Phase 1 (Setup)**: 2 tasks
- **Phase 2 (Foundational)**: 3 tasks
- **Phase 3 (US1 — Auth)**: 10 tasks
- **Phase 4 (US2 — View/Create)**: 11 tasks
- **Phase 5 (US3 — Edit/Delete)**: 9 tasks
- **Phase 6 (US4 — Complete)**: 2 tasks
- **Phase 7 (US5 — Responsive)**: 2 tasks
- **Phase 8 (Polish)**: 6 tasks
- **Parallel opportunities**: 12 tasks marked [P], plus cross-story parallelism
- **Suggested MVP scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 — Auth)
- **Format validation**: All 45 tasks follow checklist format (checkbox, ID, labels, file paths) ✅
