# Multi-stage build: compile the Vite SPA, then serve it as static files via nginx.
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
# VITE_* are embedded at build time and are PUBLIC in the resulting bundle.
# Pass them as build args (see docker-compose.vps.yml). VITE_API_KEY is only
# acceptable for internal staging behind restricted access; real auth = P10.
ARG VITE_API_BASE_URL
ARG VITE_API_KEY
ARG VITE_ACTOR_ROLE=admin
ARG VITE_ACTOR_ID=vps-admin
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL \
    VITE_API_KEY=$VITE_API_KEY \
    VITE_ACTOR_ROLE=$VITE_ACTOR_ROLE \
    VITE_ACTOR_ID=$VITE_ACTOR_ID
RUN npm run build

FROM nginx:alpine AS serve
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
