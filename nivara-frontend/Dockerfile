# ── Stage 1: BUILD ────────────────────────────────────────────────
# Installs all deps (including devDependencies) and compiles the app
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files and install ALL dependencies (including devDeps for build)
COPY package.json package-lock.json ./
RUN npm ci

# Copy source code and build the Next.js production bundle
COPY . .
RUN npm run build

# ── Stage 2: RUNNER ───────────────────────────────────────────────
# Starts fresh - only copies what's needed to SERVE the app
# Dev dependencies, source files, etc. are left behind from Stage 1
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Copy only the built output and runtime dependencies from the builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

EXPOSE 3000

# Start Next.js in production mode
CMD ["npm", "start"]
