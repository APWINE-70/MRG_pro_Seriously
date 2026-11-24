# Dockerfile for Lanna Power Outage Dashboard (Mission E: 3.5.5)
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# Copy prebuilt Next.js bundle and public assets
COPY .next/standalone ./
COPY .next/static ./.next/static
COPY public ./public

EXPOSE 3000

CMD ["node", "server.js"]
