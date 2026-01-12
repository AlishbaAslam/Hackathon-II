# Tasks: Frontend UI for Todo Web Application (2026 UI Upgrade)

**Feature**: Frontend UI for Todo Web Application (2026 UI Upgrade)
**Branch**: `001-frontend-ui`
**Generated**: 2026-01-08
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Implementation Strategy

This upgrade transforms the existing functional todo app frontend into a professional SaaS-style UI with 2026 design trends. The implementation follows the plan phases and preserves all existing functionality while elevating visual quality.

**Task Format**: Each task follows the format: `- [ ] T### Description with file path`

**Parallel Opportunities**: Tasks marked with [P] can be executed in parallel as they work on different files/components without dependencies.

## Dependencies

- **Foundation Phase** must complete before other phases
- **Home Page** can be developed in parallel with **Auth Pages**
- **UI Components** can be developed in parallel with **Pages**
- **Animation components** are dependencies for all animated pages

---

## Phase 1: Foundation Setup

- [ ] T001 [P] Create frontend/ directory structure per plan.md
- [ ] T002 [P] Copy package.json with all dependencies (Next.js 16, React 18, Tailwind CSS 3.3, Framer Motion 12.x)
- [ ] T003 [P] Copy tsconfig.json and next.config.js configurations
- [ ] T004 [P] Copy globals.css with Tailwind imports and 2026 design tokens
- [ ] T005 [P] Copy lib/types.ts with all TypeScript interfaces
- [ ] T006 [P] Copy contexts/AuthContext.tsx with authentication logic
- [ ] T007 [P] Copy hooks/useAuth.ts and hooks/useTasks.ts hooks
- [ ] T008 [P] Copy lib/api.ts with centralized API client
- [ ] T009 [P] Copy services/auth-service.ts and services/task-service.ts
- [ ] T010 [P] Copy .eslintrc.json and .prettierrc configurations

## Phase 2: Global Styles & Design Tokens

- [ ] T020 Update frontend/app/globals.css with 2026 color palette
- [ ] T021 Add CSS custom properties for purple/blue glow effects
- [ ] T022 Implement custom scrollbar styles
- [ ] T023 Add focus-visible styles for accessibility
- [ ] T024 Implement reduced motion media query support
- [ ] T025 Add typography hierarchy styles (h1-h6, body, small)
- [ ] T026 Create button focus ring glow effects
- [ ] T027 Add input field animation styles

## Phase 3: Base UI Components

- [ ] T030 [P] Create frontend/components/ui/Button.tsx with glow hover effects
- [ ] T031 [P] Create frontend/components/ui/Input.tsx with floating label animation
- [ ] T032 [P] Create frontend/components/ui/Alert.tsx dismissible notification component
- [ ] T033 [P] Create frontend/components/ui/Modal.tsx with scale/opacity animation
- [ ] T034 [P] Create frontend/components/ui/Footer.tsx footer component

## Phase 4: Layout Components

- [ ] T040 [P] Create frontend/components/layout/Navbar.tsx navigation with auth state
- [ ] T041 [P] Create frontend/components/layout/PageTransition.tsx page wrapper animations
- [ ] T042 Update frontend/app/layout.tsx to include new layout components
- [ ] T043 Update frontend/app/(auth)/layout.tsx for auth pages

## Phase 5: Auth Components (Animated)

- [ ] T050 [P] Upgrade frontend/components/auth/LoginForm.tsx with input animations
- [ ] T051 [P] Upgrade frontend/components/auth/SignupForm.tsx with input animations
- [ ] T052 Add floating labels to auth form inputs
- [ ] T053 Add button glow effects on auth forms
- [ ] T054 Add error message slide-in animations
- [ ] T055 Add loading spinner to submit buttons

## Phase 6: Home Page (New Design)

- [X] T060 Upgrade frontend/app/page.tsx with new hero section
- [ ] T061 Implement gradient background for hero section
- [ ] T062 Add animated CTA buttons with scale + glow effects
- [X] T063 Create feature cards with hover glow effects
- [ ] T064 Add feature icons with visual styling
- [ ] T065 Implement responsive grid for feature cards
- [ ] T066 Integrate Footer component into home page
- [X] T067 Add page load fade-in animations (Framer Motion)
- [X] T068 Add staggered animations for feature cards

## Phase 7: Task Components (Animated)

- [ ] T070 [P] Create frontend/components/tasks/TaskCard.tsx with hover reveal
- [ ] T071 [P] Create frontend/components/tasks/TaskList.tsx with filter tabs
- [ ] T072 [P] Create frontend/components/tasks/TaskForm.tsx with slide animation
- [ ] T073 Implement task card lift effect on hover
- [ ] T074 Implement edit/delete buttons reveal on hover
- [ ] T075 Add staggered fade-in for task list items
- [ ] T076 Add task completion visual distinction (strikethrough, opacity)
- [ ] T077 Implement filter tabs with active state animations

## Phase 8: Dashboard & Task Pages

- [ ] T080 Update frontend/app/dashboard/page.tsx with animated content
- [ ] T081 Upgrade frontend/app/tasks/page.tsx with new task components
- [ ] T082 Integrate TaskCard components into tasks page
- [ ] T083 Integrate TaskForm with animated appearance
- [ ] T084 Add dismissible Alert component for errors
- [ ] T085 Implement loading skeleton states
- [ ] T086 Add empty state with helpful guidance

## Phase 9: Page Animations

- [ ] T090 Create page transition animations (fade-in + slide)
- [ ] T091 Implement list item stagger animations
- [ ] T092 Add form expand/collapse animations
- [ ] T093 Implement modal open/close animations
- [ ] T094 Add button press/tap animations
- [ ] T095 Add success/error state animations

## Phase 10: Accessibility & Polish

- [ ] T100 Add ARIA labels to all icon-only buttons
- [ ] T101 Implement keyboard navigation for all interactive elements
- [ ] T102 Add focus management for modals and forms
- [ ] T103 Verify color contrast meets WCAG 2.1 AA
- [ ] T104 Test reduced motion preference support
- [ ] T105 Add skip links for keyboard navigation
- [ ] T106 Ensure touch targets are minimum 44x44px
- [ ] T107 Test responsive design across breakpoints (320px - 1920px)
- [ ] T108 Add screen reader announcements for dynamic content
- [ ] T109 Final visual polish and animation tuning

## Phase 11: Verification

- [ ] T120 Verify all existing API calls still work correctly
- [ ] T121 Verify authentication flow works end-to-end
- [ ] T122 Verify task CRUD operations function correctly
- [ ] T123 Test loading, empty, and error states
- [ ] T124 Verify responsive behavior on mobile/tablet/desktop
- [ ] T125 Test keyboard navigation throughout application
- [ ] T126 Test screen reader compatibility
- [ ] T127 Verify no console errors or warnings
- [ ] T128 Run build and verify successful compilation
- [ ] T129 Final code review for cleanliness and patterns

---

## File Mapping Reference

### Core Files to Copy/Upgrade
| Source | Destination |
|--------|-------------|
| phase-II-full-stack-todo/frontend/package.json | frontend/package.json |
| phase-II-full-stack-todo/frontend/lib/types.ts | frontend/lib/types.ts |
| phase-II-full-stack-todo/frontend/contexts/AuthContext.tsx | frontend/contexts/AuthContext.tsx |
| phase-II-full-stack-todo/frontend/hooks/useAuth.ts | frontend/hooks/useAuth.ts |
| phase-II-full-stack-todo/frontend/lib/api.ts | frontend/lib/api.ts |
| phase-II-full-stack-todo/frontend/services/auth-service.ts | frontend/services/auth-service.ts |
| phase-II-full-stack-todo/frontend/services/task-service.ts | frontend/services/task-service.ts |

### New Files to Create
| File | Description |
|------|-------------|
| frontend/components/ui/Button.tsx | Animated button with glow effects |
| frontend/components/ui/Input.tsx | Input with floating labels |
| frontend/components/ui/Alert.tsx | Dismissible alert notifications |
| frontend/components/ui/Modal.tsx | Modal with animations |
| frontend/components/ui/Footer.tsx | Footer component |
| frontend/components/layout/Navbar.tsx | Navigation bar |
| frontend/components/layout/PageTransition.tsx | Page wrapper animations |
| frontend/components/tasks/TaskCard.tsx | Task item with hover reveal |
| frontend/components/tasks/TaskList.tsx | Task list with filters |
| frontend/components/tasks/TaskForm.tsx | Animated task form |

### Files to Upgrade
| File | Upgrade |
|------|---------|
| frontend/app/page.tsx | Hero + features + footer |
| frontend/app/layout.tsx | Global layout |
| frontend/app/globals.css | Design tokens + animations |
| frontend/components/auth/LoginForm.tsx | Input animations |
| frontend/components/auth/SignupForm.tsx | Input animations |
| frontend/app/tasks/page.tsx | New task components |

---

## Design System Tokens (2026)

### Colors
```css
--color-primary: #6366f1;      /* Indigo */
--color-primary-dark: #4f46e5;
--color-secondary: #3b82f6;    /* Blue */
--color-accent: #8b5cf6;       /* Violet */
--color-accent-fuchsia: #d946ef;
--color-success: #10b981;      /* Emerald */
--color-error: #f43f5e;        /* Rose */
--color-warning: #f59e0b;      /* Amber */
--background-light: #f8fafc;   /* Slate 50 */
--background-dark: #1e293b;    /* Slate 800 */
```

### Glow Effects
```css
--glow-primary: 0 0 20px rgba(99, 102, 241, 0.4);
--glow-secondary: 0 0 20px rgba(59, 130, 246, 0.4);
--glow-accent: 0 0 20px rgba(139, 92, 246, 0.4);
```

### Spacing
```css
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-2xl: 48px;
--space-3xl: 64px;
```

### Border Radius
```css
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 16px;
--radius-2xl: 24px;
```

---

## Animation Durations
- Page transitions: 0.3-0.5s
- List item stagger: 0.05-0.1s
- Hover effects: 0.2s
- Form inputs: 0.15s
- Modal/dialog: 0.2-0.3s