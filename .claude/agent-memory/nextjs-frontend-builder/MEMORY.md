# Next.js Frontend Builder - Agent Memory

## Project Setup & Structure

### Next.js 16+ App Router Project
- **Location**: `D:\GIAIC\Q-4\HACKATHON_2\PHASE-2\frontend\`
- **Framework**: Next.js 16+ with App Router (app directory)
- **TypeScript**: v5.6+ with strict mode enabled
- **Styling**: Tailwind CSS v3.4+ with mobile-first approach
- **Linting**: ESLint with next/core-web-vitals and next/typescript configs

### Key Configuration Files
1. **tsconfig.json**: Path aliases use `@/*` for root imports
2. **tailwind.config.ts**: Configured for app/, components/, pages/ directories
3. **next.config.ts**: Using TypeScript config format (not .js)
4. **postcss.config.mjs**: Standard Tailwind + Autoprefixer setup

### Directory Structure Conventions
- `app/` - App Router pages, layouts, and route handlers (Server Components by default)
- `components/` - Reusable React components (mark Client Components with 'use client')
- `lib/` - Utility functions, API clients, auth configuration
- `public/` - Static assets (images, SVGs, fonts)

### Authentication Setup
- **Better Auth v1.0+** for authentication
- Database: PostgreSQL (Neon) shared with backend
- Packages: better-auth, pg, @better-auth/cli

### Environment Variables Pattern
```
BETTER_AUTH_SECRET - Random secret for auth (use openssl rand -base64 32)
BETTER_AUTH_URL - Frontend URL (http://localhost:3000 for dev)
DATABASE_URL - PostgreSQL connection string (same as backend)
NEXT_PUBLIC_API_URL - Backend API endpoint (http://localhost:8000)
```

## Development Patterns

### Server Components First
- Default to React Server Components
- Only add 'use client' for:
  - Event handlers (onClick, onChange, etc.)
  - React hooks (useState, useEffect, useContext)
  - Browser APIs (window, document, localStorage)
  - Third-party client libraries

### Responsive Design Standards
- Mobile-first approach (default styles for mobile)
- Breakpoints: sm(640px), md(768px), lg(1024px), xl(1280px), 2xl(1536px)
- Touch targets: minimum 44x44px
- Test across: mobile (<640px), tablet (768-1024px), desktop (>1024px)

### Component Architecture
- Atomic design: atoms → molecules → organisms → templates → pages
- TypeScript interfaces for all props (no 'any' types)
- Named exports preferred over default exports
- Colocate related files when component has multiple files

### Performance Best Practices
- Use next/image for all images with proper width, height, sizes
- Use next/font for optimized font loading
- Leverage next/dynamic for heavy client components
- Fetch data in Server Components with proper cache strategies
- Include metadata export for SEO

## Installation Notes

### Manual Setup Required
- When Bash permission is denied, manually create project structure
- All configuration files created with proper TypeScript/ESLint settings
- Dependencies added to package.json (user must run npm install manually)
- Better Auth packages pre-configured in dependencies

### Files Created Checklist
- [x] package.json with all dependencies
- [x] tsconfig.json with path aliases
- [x] next.config.ts, tailwind.config.ts, postcss.config.mjs
- [x] .eslintrc.json, .gitignore
- [x] app/layout.tsx, app/page.tsx, app/globals.css
- [x] .env.example with all required variables
- [x] public/ assets (SVG files)
- [x] README.md and INSTALLATION.md
- [x] lib/ and components/ directories with .gitkeep

## Common Issues & Solutions

### Issue: Permission denied for Bash commands
**Solution**: Create files manually using Write tool, update package.json directly, provide instructions for user to run npm install

### Issue: Missing directories after creation
**Solution**: Add .gitkeep files to ensure empty directories are tracked

### Issue: Unclear project requirements
**Strategy**: Surface options to user and get explicit preference rather than assuming

## Related Documentation
- [Next.js App Router Docs](https://nextjs.org/docs/app)
- [Better Auth Docs](https://better-auth.com)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
