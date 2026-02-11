# Frontend Installation Guide

## Prerequisites

- Node.js 18.17 or later
- npm or yarn package manager

## Installation Steps

### 1. Install Dependencies

From the `frontend/` directory, run:

```bash
npm install
```

This will install:
- Next.js 16+
- React 19
- TypeScript 5.6+
- Tailwind CSS 3.4+
- Better Auth 1.0+
- PostgreSQL client (pg)
- ESLint

### 2. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env.local
```

Then edit `.env.local` with your actual values:

```env
# Better Auth
BETTER_AUTH_SECRET=your-random-secret-string-here  # Generate with: openssl rand -base64 32
BETTER_AUTH_URL=http://localhost:3000

# Database (same Neon database as backend)
DATABASE_URL=postgresql://user:pass@ep-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at [http://localhost:3000](http://localhost:3000)

### 4. Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout with fonts and metadata
│   ├── page.tsx           # Home page
│   ├── globals.css        # Global styles with Tailwind
│   └── favicon.ico        # Favicon
├── components/            # Reusable React components
│   └── .gitkeep
├── lib/                   # Utility functions and configurations
│   └── .gitkeep
├── public/                # Static assets (images, SVGs)
│   ├── next.svg
│   ├── vercel.svg
│   ├── file.svg
│   ├── globe.svg
│   └── window.svg
├── .env.example           # Environment variables template
├── .eslintrc.json         # ESLint configuration
├── .gitignore             # Git ignore rules
├── next.config.ts         # Next.js configuration
├── package.json           # Dependencies and scripts
├── postcss.config.mjs     # PostCSS configuration
├── tailwind.config.ts     # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
└── README.md              # Project documentation

## Available Scripts

- `npm run dev` - Start development server on port 3000
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Next Steps

1. Configure Better Auth by creating `lib/auth.ts`
2. Set up API client in `lib/api.ts`
3. Create reusable components in `components/`
4. Add authentication pages (login, signup, etc.)
5. Implement protected routes and layouts

## Troubleshooting

### Port Already in Use

If port 3000 is already in use, you can specify a different port:

```bash
npm run dev -- -p 3001
```

### Module Not Found

If you encounter module errors, try:

```bash
rm -rf node_modules package-lock.json
npm install
```

### Type Errors

Ensure TypeScript is properly configured:

```bash
npm run build
```

This will check for type errors across the entire project.
